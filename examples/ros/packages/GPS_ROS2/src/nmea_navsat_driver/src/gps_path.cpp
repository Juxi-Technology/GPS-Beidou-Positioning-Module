#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/nav_sat_fix.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <nav_msgs/msg/path.hpp>
#include <cmath>

struct MyPose
{
    double latitude;
    double longitude;
    double altitude;
};

double rad(double d)
{
    return d * M_PI / 180.0;
}

static const double EARTH_RADIUS = 6378.137;

class GPSPathNode : public rclcpp::Node
{
public:
    GPSPathNode() : Node("gps_path_node"), init_(false)
    {
        state_pub_ = this->create_publisher<nav_msgs::msg::Path>("gps_path", 10);
        gps_sub_ = this->create_subscription<sensor_msgs::msg::NavSatFix>(
            "/fix", 10, std::bind(&GPSPathNode::gpsCallback, this, std::placeholders::_1));
        ros_path_.header.frame_id = "path";
    }

private:
    void gpsCallback(const sensor_msgs::msg::NavSatFix::SharedPtr gps_msg_ptr)
    {
        if (!init_)
        {
            init_pose_.latitude = gps_msg_ptr->latitude;
            init_pose_.longitude = gps_msg_ptr->longitude;
            init_pose_.altitude = gps_msg_ptr->altitude;
            init_ = true;
            RCLCPP_INFO(this->get_logger(), "Initial GPS position received");
        }
        else
        {
            double radLat1, radLat2, radLong1, radLong2, delta_lat, delta_long, x, y;
            radLat1 = rad(init_pose_.latitude);
            radLong1 = rad(init_pose_.longitude);
            radLat2 = rad(gps_msg_ptr->latitude);
            radLong2 = rad(gps_msg_ptr->longitude);

            delta_lat = radLat2 - radLat1;
            delta_long = 0;
            if (delta_lat > 0)
                x = -2 * asin(sqrt(pow(sin(delta_lat / 2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(delta_long / 2), 2)));
            else
                x = -2 * asin(sqrt(pow(sin(delta_lat / 2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(delta_long / 2), 2)));
            x = x * EARTH_RADIUS * 1000;

            delta_lat = 0;
            delta_long = radLong2 - radLong1;
            if (delta_long > 0)
                y = 2 * asin(sqrt(pow(sin(delta_lat / 2), 2) + cos(radLat2) * cos(radLat2) * pow(sin(delta_long / 2), 2)));
            else
                y = -2 * asin(sqrt(pow(sin(delta_lat / 2), 2) + cos(radLat2) * cos(radLat2) * pow(sin(delta_long / 2), 2)));
            y = y * EARTH_RADIUS * 1000;

            double z = gps_msg_ptr->altitude - init_pose_.altitude;

            ros_path_.header.stamp = this->now();

            geometry_msgs::msg::PoseStamped pose;
            pose.header = ros_path_.header;
            pose.pose.position.x = x;
            pose.pose.position.y = y;
            pose.pose.position.z = z;

            ros_path_.poses.push_back(pose);

            RCLCPP_INFO(this->get_logger(), "( x:%.6f , y:%.6f , z:%.6f )", x, y, z);

            state_pub_->publish(ros_path_);
        }
    }

    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr state_pub_;
    rclcpp::Subscription<sensor_msgs::msg::NavSatFix>::SharedPtr gps_sub_;
    nav_msgs::msg::Path ros_path_;
    bool init_;
    MyPose init_pose_;
};

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<GPSPathNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
