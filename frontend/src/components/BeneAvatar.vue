<template>
  <div
    class="bene-avatar"
    :class="[`bene-avatar--${size}`, { 'bene-avatar--breathing': breathing }]"
  >
    <img
      src="../assets/bene-avatar.png"
      alt="Seu Bené"
      class="bene-avatar__img"
    />
  </div>
</template>

<script>
export default {
  name: 'BeneAvatar',
  props: {
    size: {
      type: String,
      default: 'floating',
      validator: (v) => ['small', 'medium', 'floating'].includes(v),
    },
    breathing: {
      type: Boolean,
      default: true,
    },
  },
}
</script>

<style scoped>
.bene-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.bene-avatar__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

.bene-avatar--small {
  width: 28px;
  height: 28px;
}

.bene-avatar--medium {
  width: 40px;
  height: 40px;
}

.bene-avatar--floating {
  width: 68px;
  height: 68px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
  cursor: pointer;
  opacity: 0.92;
  transition: all 0.4s ease;
}

.bene-avatar--floating:hover {
  opacity: 1;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35), 0 0 24px rgba(34, 197, 94, 0.06);
  transform: scale(1.04);
}

.bene-avatar--breathing.bene-avatar--floating {
  animation: beneBreathe 5s ease-in-out infinite;
}

.bene-avatar--breathing.bene-avatar--floating:hover {
  animation-play-state: paused;
}

@keyframes beneBreathe {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.015);
  }
}
</style>
