<script>
  export let score;
  export let total;
  export let examName;
  export let onRetry = () => {};
  export let onBack = () => {};

  $: pct = Math.round((score / total) * 100);
  $: grade = pct >= 90 ? '🏆 Ottimo!' : pct >= 70 ? '👍 Buono!' : pct >= 50 ? '📖 Continua a studiare' : '💪 Riprova!';
</script>

<div class="page">
  <header>
    <h2>Quiz completato!</h2>
    <p class="exam-name">{examName}</p>
  </header>

  <div class="score-card">
    <div class="score-circle">
      <span class="score-num">{score}</span>
      <span class="score-div">/</span>
      <span class="score-tot">{total}</span>
    </div>
    <p class="score-pct">{pct}%</p>
    <p class="grade">{grade}</p>
  </div>

  <div class="actions">
    <button class="retry-btn" on:click={onRetry}>🔁 Rifai questo quiz</button>
    <button class="back-btn" on:click={onBack}>← Scegli altro esame</button>
  </div>
</div>

<style>
  .page {
    max-width: 480px;
    margin: 0 auto;
    padding: 2rem 1rem;
    text-align: center;
  }

  header { margin-bottom: 2rem; }
  h2 { font-size: 1.6rem; margin: 0 0 0.25rem; }
  .exam-name { color: var(--color-muted); margin: 0; }

  .score-card {
    background: var(--color-card);
    border: 1px solid var(--color-border);
    border-radius: 16px;
    padding: 2rem 1rem;
    margin-bottom: 2rem;
  }

  .score-circle {
    display: inline-flex;
    align-items: baseline;
    gap: 0.2rem;
    margin-bottom: 0.5rem;
  }

  .score-num {
    font-size: 4rem;
    font-weight: 800;
    color: var(--color-primary);
    line-height: 1;
  }

  .score-div {
    font-size: 2.5rem;
    color: var(--color-muted);
  }

  .score-tot {
    font-size: 2rem;
    color: var(--color-muted);
  }

  .score-pct {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--color-muted);
    margin: 0.25rem 0 0;
  }

  .grade {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0.75rem 0 0;
  }

  .actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .retry-btn {
    padding: 0.9rem;
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.15s;
  }

  .retry-btn:hover { opacity: 0.88; }

  .back-btn {
    padding: 0.75rem;
    background: none;
    color: var(--color-primary);
    border: 2px solid var(--color-border);
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: border-color 0.15s;
  }

  .back-btn:hover { border-color: var(--color-primary); }
</style>
