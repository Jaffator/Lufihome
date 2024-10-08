import { socket } from "@/socket";

export default function socketPlugin() {
  return (store) => {
    // ------- to alarm store -------
    socket.on("areasUpdate", (data) => {
      store.commit("alarm/updateAreas", data);
    });
    socket.on("updateAlarmEvents", (data) => {
      store.dispatch("events/getUnreadMsg_alarm");
    });
    socket.on("broadcast_updatedAreas", (data) => {
      store.commit("alarm/updateAreas", data);
    });
    socket.on("broadcast_houseall", (data) => {
      store.commit("alarm/houseSwitch", data);
    });
    socket.on("broadcast_nightmode", (data) => {
      store.commit("alarm/nightmodeSwitch", data);
    });
    socket.on("broadcast_setting", (data) => {
      for (var key in data) {
        if (data[key].Name == "AlarmState") {
          store.commit("alarm/changeAlarmState", data[key].Value);
        }
      }
    });
    socket.on("reset_origin", () => {
      store.commit("alarm/changeOrigin", false);
    });
    // ------- to sensors store -------
    socket.on("broadcast_sensorState", (data) => {
      store.commit("sensors/updateSensorState", data);
    });
    socket.on("broadcast_gateState", (data) => {
      store.commit("sensors/updateGateState", data);
    });
  };
}
