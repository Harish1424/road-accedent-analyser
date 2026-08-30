def get_resource_recommendations(predicted_risk, weather_condition, road_type):
    risk_actions = []
    if predicted_risk == "High":
        risk_actions = [
            "High Patrol Deployment: Dispatch emergency highway patrol units to key high-risk corridors.",
            "Speed Control: Setup radar speed traps and automated speed governor checkpoints.",
            "Traffic Signals: Enable emergency flashing beacons and signal priority overrides.",
            "Medical Preparedness: Position mobile ambulances at 5km radii along the target road network."
        ]
    elif predicted_risk == "Medium":
        risk_actions = [
            "Routine Patrols: Increase stationary police presence during peak bottleneck hours.",
            "Signage & Alerts: Activate variable message signs warning drivers of upcoming hazards.",
            "Visibility & Maintenance: Inspect street light operations and lane markings."
        ]
    else:
        risk_actions = [
            "Automated Surveillance: Monitor traffic flow using standard CCTV feeds.",
            "Routine Patrol: Continue baseline shift coverage without additional unit deployment."
        ]
        
    env_actions = []
    if weather_condition in ["Rainy", "Stormy"]:
        env_actions.append("Issue wet-pavement slick road advisories and reduce variable speed limits by 15 mph.")
    if weather_condition == "Foggy":
        env_actions.append("Activate high-intensity fog warning beacons and illuminate road reflectors.")
    if road_type in ["Highway", "Expressway"]:
        env_actions.append("Enforce heavy vehicle lane restrictions and ramp metering control.")
    if road_type == "Intersection":
        env_actions.append("Deploy traffic wardens to assist signal cycles and prevent box-blocking.")
    if not env_actions:
        env_actions.append("Standard road conditions detected. No dynamic weather advisories required.")
        
    return risk_actions, env_actions
