#include <memory>

#include "rclcpp/rclcpp.hpp"

#include "imu_gps_localization/localization_wrapper.h"

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);

    auto node = std::make_shared<LocalizationWrapper>();

    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}
