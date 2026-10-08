#include "imu_gps_localization/localization_wrapper.h"

#include <iomanip>

#include "tf2/LinearMath/Quaternion.h"

LocalizationWrapper::LocalizationWrapper()
    : Node("imu_gps_localization_node") {

    double acc_noise, gyro_noise, acc_bias_noise, gyro_bias_noise;
    this->declare_parameter("acc_noise", 1e-2);
    this->declare_parameter("gyro_noise", 1e-4);
    this->declare_parameter("acc_bias_noise", 1e-6);
    this->declare_parameter("gyro_bias_noise", 1e-8);
    this->get_parameter("acc_noise", acc_noise);
    this->get_parameter("gyro_noise", gyro_noise);
    this->get_parameter("acc_bias_noise", acc_bias_noise);
    this->get_parameter("gyro_bias_noise", gyro_bias_noise);

    double x, y, z;
    this->declare_parameter("I_p_Gps_x", 0.0);
    this->declare_parameter("I_p_Gps_y", 0.0);
    this->declare_parameter("I_p_Gps_z", 0.0);
    this->get_parameter("I_p_Gps_x", x);
    this->get_parameter("I_p_Gps_y", y);
    this->get_parameter("I_p_Gps_z", z);
    const Eigen::Vector3d I_p_Gps(x, y, z);

    std::string log_folder = "/tmp";
    this->declare_parameter("log_folder", log_folder);
    this->get_parameter("log_folder", log_folder);

    file_state_.open(log_folder + "/state.csv");
    file_gps_.open(log_folder + "/gps.csv");

    imu_gps_localizer_ptr_ =
        std::make_unique<ImuGpsLocalization::ImuGpsLocalizer>(acc_noise, gyro_noise,
                                                              acc_bias_noise, gyro_bias_noise,
                                                              I_p_Gps);

    imu_sub_ = this->create_subscription<sensor_msgs::msg::Imu>(
        "/imu/data", 10,
        std::bind(&LocalizationWrapper::ImuCallback, this, std::placeholders::_1));

    gps_position_sub_ = this->create_subscription<sensor_msgs::msg::NavSatFix>(
        "/fix", 10,
        std::bind(&LocalizationWrapper::GpsPositionCallback, this, std::placeholders::_1));

    path_pub_ = this->create_publisher<nav_msgs::msg::Path>("/fused_path", 10);

    RCLCPP_INFO(this->get_logger(), "Imu GPS Localization Node Started!");
}

LocalizationWrapper::~LocalizationWrapper() {
    file_state_.close();
    file_gps_.close();
}

void LocalizationWrapper::ImuCallback(const sensor_msgs::msg::Imu::SharedPtr imu_msg_ptr) {
    ImuGpsLocalization::ImuDataPtr imu_data_ptr = std::make_shared<ImuGpsLocalization::ImuData>();
    imu_data_ptr->timestamp = imu_msg_ptr->header.stamp.sec + imu_msg_ptr->header.stamp.nanosec * 1e-9;
    imu_data_ptr->acc << imu_msg_ptr->linear_acceleration.x,
                         imu_msg_ptr->linear_acceleration.y,
                         imu_msg_ptr->linear_acceleration.z;
    imu_data_ptr->gyro << imu_msg_ptr->angular_velocity.x,
                          imu_msg_ptr->angular_velocity.y,
                          imu_msg_ptr->angular_velocity.z;

    ImuGpsLocalization::State fused_state;
    const bool ok = imu_gps_localizer_ptr_->ProcessImuData(imu_data_ptr, &fused_state);
    if (!ok) {
        return;
    }

    ConvertStateToRosTopic(fused_state);
    path_pub_->publish(ros_path_);

    LogState(fused_state);
}

void LocalizationWrapper::GpsPositionCallback(const sensor_msgs::msg::NavSatFix::SharedPtr gps_msg_ptr) {
    if (gps_msg_ptr->status.status != 2) {
        RCLCPP_WARN(this->get_logger(), "Bad gps message!");
        return;
    }

    ImuGpsLocalization::GpsPositionDataPtr gps_data_ptr = std::make_shared<ImuGpsLocalization::GpsPositionData>();
    gps_data_ptr->timestamp = gps_msg_ptr->header.stamp.sec + gps_msg_ptr->header.stamp.nanosec * 1e-9;
    gps_data_ptr->lla << gps_msg_ptr->latitude,
                         gps_msg_ptr->longitude,
                         gps_msg_ptr->altitude;
    gps_data_ptr->cov = Eigen::Map<const Eigen::Matrix3d>(gps_msg_ptr->position_covariance.data());

    imu_gps_localizer_ptr_->ProcessGpsPositionData(gps_data_ptr);

    LogGps(gps_data_ptr);
}

void LocalizationWrapper::LogState(const ImuGpsLocalization::State& state) {
    const Eigen::Quaterniond G_q_I(state.G_R_I);
    file_state_ << std::fixed << std::setprecision(15)
                << state.timestamp << ","
                << state.lla[0] << "," << state.lla[1] << "," << state.lla[2] << ","
                << state.G_p_I[0] << "," << state.G_p_I[1] << "," << state.G_p_I[2] << ","
                << state.G_v_I[0] << "," << state.G_v_I[1] << "," << state.G_v_I[2] << ","
                << G_q_I.x() << "," << G_q_I.y() << "," << G_q_I.z() << "," << G_q_I.w() << ","
                << state.acc_bias[0] << "," << state.acc_bias[1] << "," << state.acc_bias[2] << ","
                << state.gyro_bias[0] << "," << state.gyro_bias[1] << "," << state.gyro_bias[2] << "\n";
}

void LocalizationWrapper::LogGps(const ImuGpsLocalization::GpsPositionDataPtr gps_data) {
    file_gps_ << std::fixed << std::setprecision(15)
              << gps_data->timestamp << ","
              << gps_data->lla[0] << "," << gps_data->lla[1] << "," << gps_data->lla[2] << "\n";
}

void LocalizationWrapper::ConvertStateToRosTopic(const ImuGpsLocalization::State& state) {
    ros_path_.header.frame_id = "world";
    ros_path_.header.stamp = this->now();

    geometry_msgs::msg::PoseStamped pose;
    pose.header = ros_path_.header;

    pose.pose.position.x = state.G_p_I[0];
    pose.pose.position.y = state.G_p_I[1];
    pose.pose.position.z = state.G_p_I[2];

    const Eigen::Quaterniond G_q_I(state.G_R_I);
    pose.pose.orientation.x = G_q_I.x();
    pose.pose.orientation.y = G_q_I.y();
    pose.pose.orientation.z = G_q_I.z();
    pose.pose.orientation.w = G_q_I.w();

    ros_path_.poses.push_back(pose);
}
