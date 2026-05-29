<template>
  <div class="statement-empty">
    <div class="statement-empty__icon">📊</div>
    <h3 class="statement-empty__title">
      Teu extrato ainda tá vazio
    </h3>
    <p class="statement-empty__description">
      Bora registrar tua primeira despesa ou receita pra começar a acompanhar teu histórico financeiro?
    </p>
  </div>
</template>

<script setup>
</script>

<style scoped>
.statement-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  gap: 12px;
}

.statement-empty__icon {
  font-size: 40px;
  opacity: 0.4;
  margin-bottom: 4px;
}

.statement-empty__title {
  font-size: 16px;
  font-weight: 500;
  color: #94a3b8;
  margin: 0;
}

.statement-empty__description {
  font-size: 13px;
  color: #475569;
  max-width: 280px;
  line-height: 1.5;
  margin: 0;
}

.statement-empty__action {
  margin-top: 4px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: #64748b;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.statement-empty__action:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}

@media (max-width: 768px) {
  .statement-empty {
    padding: 32px 20px;
  }

  .statement-empty__icon {
    font-size: 32px;
  }

  .statement-empty__title {
    font-size: 15px;
  }

  .statement-empty__description {
    font-size: 12px;
  }
}
</style>
