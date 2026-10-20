#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <lab_interfaces/msg/telemetry.hpp>

class Monitor final : public rclcpp::Node {
public:
  Monitor() : Node("monitor") {
    declare_parameter<double>("low_voltage", 11.9);
    subscription_ = create_subscription<lab_interfaces::msg::Telemetry>(
      "telemetry", rclcpp::QoS(10).reliable(),
      [this](lab_interfaces::msg::Telemetry::ConstSharedPtr msg) {
        const auto threshold = get_parameter("low_voltage").as_double();
        if (msg->voltage < threshold) {
          RCLCPP_WARN(get_logger(), "LOW seq=%u voltage=%.2f threshold=%.2f",
                      msg->sequence, msg->voltage, threshold);
        } else {
          RCLCPP_INFO(get_logger(), "OK seq=%u voltage=%.2f", msg->sequence, msg->voltage);
        }
      });
  }
private:
  rclcpp::Subscription<lab_interfaces::msg::Telemetry>::SharedPtr subscription_;
};

int main(int argc, char ** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Monitor>());
  rclcpp::shutdown();
  return 0;
}
