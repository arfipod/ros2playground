#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <lab_interfaces/msg/telemetry.hpp>

class Monitor final : public rclcpp::Node {
public:
  Monitor() : Node("monitor") {
    subscription_ = create_subscription<lab_interfaces::msg::Telemetry>(
      "telemetry", rclcpp::QoS(10).reliable(),
      [this](lab_interfaces::msg::Telemetry::ConstSharedPtr msg) {
        RCLCPP_INFO(get_logger(), "seq=%u voltage=%.2f V temperature=%.2f C",
                    msg->sequence, msg->voltage, msg->temperature);
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
