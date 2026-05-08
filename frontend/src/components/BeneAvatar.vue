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
  width: 80px;
  height: 80px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3), 0 0 0 2px rgba(255, 255, 255, 0.06);
  cursor: pointer;
}

.bene-avatar--floating:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(255, 255, 255, 0.1);
}

.bene-avatar--breathing.bene-avatar--floating {
  animation: beneBreathe 4s ease-in-out infinite;
}

@keyframes beneBreathe {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.03);
  }
}
</style>
