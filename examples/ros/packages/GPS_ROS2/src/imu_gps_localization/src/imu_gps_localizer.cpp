#include "imu_gps_localization/imu_gps_localizer.h"

#include <iostream>

#include "imu_gps_localization/utils.h"

namespace ImuGpsLocalization {

ImuGpsLocalizer::ImuGpsLocalizer(const double acc_noise, const double gyro_noise,
                                 const double acc_bias_noise, const double gyro_bias_noise,
                                 const Eigen::Vector3d& I_p_Gps)
    : initialized_(false) {
    initializer_ = std::make_unique<Initializer>(I_p_Gps);
    imu_processor_ = std::make_unique<ImuProcessor>(acc_noise, gyro_noise,
                                                    acc_bias_noise, gyro_bias_noise,
                                                    Eigen::Vector3d(0.0, 0.0, -9.81007));
    gps_processor_ = std::make_unique<GpsProcessor>(I_p_Gps);
}

bool ImuGpsLocalizer::ProcessImuData(const ImuDataPtr imu_data_ptr, State* fused_state) {
    if (!initialized_) {
        initializer_->AddImuData(imu_data_ptr);
        return false;
    }

    imu_processor_->Predict(state_.imu_data_ptr, imu_data_ptr, &state_);

    ConvertENUToLLA(init_lla_, state_.G_p_I, &(state_.lla));
    *fused_state = state_;
    return true;
}

bool ImuGpsLocalizer::ProcessGpsPositionData(const GpsPositionDataPtr gps_data_ptr) {
    if (!initialized_) {
        if (!initializer_->AddGpsPositionData(gps_data_ptr, &state_)) {
            return false;
        }

        init_lla_ = gps_data_ptr->lla;

        initialized_ = true;

        std::cout << "[ImuGpsLocalizer] System initialized!" << std::endl;
        return true;
    }

    gps_processor_->UpdateStateByGpsPosition(init_lla_, gps_data_ptr, &state_);

    return true;
}

}
