<template>
  <div class="base-timer">
    <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g class="base-timer__circle">
        <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
        <path
          :stroke-dasharray="circleDasharray"
          class="base-timer__path-remaining"
          :class="remainingPathColor"
          d="
              M 50, 50
              m -45, 0
              a 45,45 0 1,0 90,0
              a 45,45 0 1,0 -90,0
            "
        ></path>
      </g>
    </svg>
    <span class="base-timer__label">{{ formattedTimeLeft }}</span>
  </div>
</template>

<script>
import { mapState } from "vuex";
const FULL_DASH_ARRAY = 283;
const WARNING_THRESHOLD = 10;
const ALERT_THRESHOLD = 5;

const COLOR_CODES = {
  info: {
    color: "green",
  },
  warning: {
    color: "orange",
    threshold: WARNING_THRESHOLD,
  },
  alert: {
    color: "red",
    threshold: ALERT_THRESHOLD,
  },
};

const TIME_LIMIT = 60;

export default {
  data() {
    return {
      timePassed: 0,
      timerInterval: null,
      time_lim: 0,
    };
  },

  computed: {
    circleDasharray() {
      return `${(this.timeFraction * FULL_DASH_ARRAY).toFixed(0)} 283`;
    },

    formattedTimeLeft() {
      const timeLeft = this.timeLeft;
      const minutes = Math.floor(timeLeft / 60);
      let seconds = timeLeft % 60;

      if (seconds < 10) {
        seconds = `0${seconds}`;
      }

      return `${minutes}:${seconds}`;
    },

    timeLeft() {
      return this.time_lim - this.timePassed;
    },

    timeFraction() {
      const rawTimeFraction = this.timeLeft / this.time_lim;
      return rawTimeFraction - (1 / this.time_lim) * (1 - rawTimeFraction);
    },

    remainingPathColor() {
      const { alert, warning, info } = COLOR_CODES;

      if (this.timeLeft <= alert.threshold) {
        return alert.color;
      } else if (this.timeLeft <= warning.threshold) {
        return warning.color;
      } else {
        return info.color;
      }
    },
  },

  watch: {
    timeLeft(newValue) {
      if (newValue === 0) {
        this.onTimesUp();
      }
    },
  },

  mounted() {
    this.time_lim = this.$store.state.alarm.armTime;
    this.startTimer();
  },

  methods: {
    // ----------------------------------- TimesUp -> send request to server -----------------------------------
    onTimesUp() {
      clearInterval(this.timerInterval);
      if (this.$store.state.alarm.origin) {
        this.$store.dispatch("alarm/houseall");
        this.$store.dispatch("alarm/nightmode");
        this.$emit("TimesUp");
        console.log("--- times up ---");
      } else {
        console.log("--- times up not from origin ---");
      }
    },

    startTimer() {
      this.timerInterval = setInterval(() => (this.timePassed += 1), 1000);
    },
  },
};
</script>

<style scoped lang="scss">
.base-timer {
  position: relative;
  width: 40px;
  height: 40px;

  &__svg {
    transform: scaleX(-1);
  }

  &__circle {
    fill: none;
    stroke: none;
  }

  &__path-elapsed {
    stroke-width: 10px;
    stroke: #bdbdbd;
  }

  &__path-remaining {
    stroke-width: 10px;
    stroke-linecap: round;
    transform: rotate(90deg);
    transform-origin: center;
    transition: 1s linear all;
    fill-rule: nonzero;
    stroke: currentColor;

    &.green {
      color: #00e676;
    }

    &.orange {
      color: #ff6e40;
    }

    &.red {
      color: #ff5252;
    }
  }

  &__label {
    position: absolute;
    width: 40px;
    height: 40px;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
  }
}
</style>
