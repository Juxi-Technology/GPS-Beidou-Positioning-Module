#pragma once

#include <fstream>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"
#include "nav_msgs/msg/path.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"

#include "imu_gps_localization/imu_gps_localizer.h"

class LocalizationWrapper : public rclcpp::Node {
public:
    LocalizationWrapper();
    ~LocalizationWrapper();

private:
    void ImuCallback(const sensor_msgs::msg::Imu::SharedPtr imu_msg_ptr);

    void GpsPositionCallback(const sensor_msgs::msg::NavSatFix::SharedPtr gps_msg_ptr);

    void LogState(const ImuGpsLocalization::State& state);
    void LogGps(const ImuGpsLocalization::GpsPositionDataPtr gps_data);

    void ConvertStateToRosTopic(const ImuGpsLocalization::State& state);

    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub_;
    rclcpp::Subscription<sensor_msgs::msg::NavSatFix>::SharedPtr gps_position_sub_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;

    std::ofstream file_state_;
    std::ofstream file_gps_;

    nav_msgs::msg::Path ros_path_;

    std::unique_ptr<ImuGpsLocalization::ImuGpsLocalizer> imu_gps_localizer_ptr_;
};
