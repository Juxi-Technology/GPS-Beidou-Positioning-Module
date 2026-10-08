#include "imu_gps_localization/initializer.h"

#include <Eigen/Dense>
#include <iostream>

#include "imu_gps_localization/utils.h"

namespace ImuGpsLocalization {

Initializer::Initializer(const Eigen::Vector3d& init_I_p_Gps)
    : init_I_p_Gps_(init_I_p_Gps) { }

void Initializer::AddImuData(const ImuDataPtr imu_data_ptr) {
    imu_buffer_.push_back(imu_data_ptr);

    if (imu_buffer_.size() > kImuDataBufferLength) {
        imu_buffer_.pop_front();
    }
}

bool Initializer::AddGpsPositionData(const GpsPositionDataPtr gps_data_ptr, State* state) {
    if (imu_buffer_.size() < kImuDataBufferLength) {
        std::cerr << "[Initializer] No enough imu data!" << std::endl;
        return false;
    }

    const ImuDataPtr last_imu_ptr = imu_buffer_.back();
    if (std::abs(gps_data_ptr->timestamp - last_imu_ptr->timestamp) > 0.5) {
        std::cerr << "[Initializer] Gps and imu timestamps are not synchronized!" << std::endl;
        return false;
    }

    state->timestamp = last_imu_ptr->timestamp;
    state->imu_data_ptr = last_imu_ptr;

    state->G_p_I.setZero();
    state->G_v_I.setZero();

    if (!ComputeG_R_IFromImuData(&state->G_R_I)) {
        std::cerr << "[Initializer] Failed to compute G_R_I!" << std::endl;
        return false;
    }

    state->acc_bias.setZero();
    state->gyro_bias.setZero();

    state->cov.setZero();
    state->cov.block<3, 3>(0, 0) = 100.0 * Eigen::Matrix3d::Identity();
    state->cov.block<3, 3>(3, 3) = 100.0 * Eigen::Matrix3d::Identity();
    state->cov.block<2, 2>(6, 6) = 10.0 * kDegreeToRadian * 10.0 * kDegreeToRadian * Eigen::Matrix2d::Identity();
    state->cov(8, 8) = 100.0 * kDegreeToRadian * 100.0 * kDegreeToRadian;
    state->cov.block<3, 3>(9, 9) = 0.0004 * Eigen::Matrix3d::Identity();
    state->cov.block<3, 3>(12, 12) = 0.0004 * Eigen::Matrix3d::Identity();

    return true;
}

bool Initializer::ComputeG_R_IFromImuData(Eigen::Matrix3d* G_R_I) {
    Eigen::Vector3d sum_acc(0.0, 0.0, 0.0);
    for (const auto& imu_data : imu_buffer_) {
        sum_acc += imu_data->acc;
    }
    const Eigen::Vector3d mean_acc = sum_acc / (double)imu_buffer_.size();

    Eigen::Vector3d sum_err2(0.0, 0.0, 0.0);
    for (const auto& imu_data : imu_buffer_) {
        sum_err2 += (imu_data->acc - mean_acc).cwiseAbs2();
    }
    const Eigen::Vector3d std_acc = (sum_err2 / (double)imu_buffer_.size()).cwiseSqrt();

    if (std_acc.maxCoeff() > kAccStdLimit) {
        std::cerr << "[Initializer] Too big acc std: " << std_acc(0) << ", " << std_acc(1) << ", " << std_acc(2) << std::endl;
        return false;
    }

    const Eigen::Vector3d& z_axis = mean_acc.normalized();

    Eigen::Vector3d x_axis =
        Eigen::Vector3d::UnitX() - z_axis * z_axis.transpose() * Eigen::Vector3d::UnitX();
    x_axis.normalize();

    Eigen::Vector3d y_axis = z_axis.cross(x_axis);
    y_axis.normalize();

    Eigen::Matrix3d I_R_G;
    I_R_G.block<3, 1>(0, 0) = x_axis;
    I_R_G.block<3, 1>(0, 1) = y_axis;
    I_R_G.block<3, 1>(0, 2) = z_axis;

    *G_R_I = I_R_G.transpose();

    return true;
}

}
