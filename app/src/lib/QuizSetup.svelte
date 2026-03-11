<script>
  export let exam;
  export let totalQuestions = 0;
  export let onStart = () => {};
  export let onBack = () => {};

  const presets = [10, 20, 30];
  let selected = null;
  let custom = '';

  $: count = selected === 'all'
    ? totalQuestions
    : selected !== null
      ? selected
      : (() => { const n = parseInt(custom, 10); return isNaN(n) || n < 1 ? null : Math.min(n, totalQuestions); })();

  function start() {
    if (count) onStart(count);
  }
</script>

<div class="page">
  <button class="back-btn" on:click={onBack}>← Indietro</button>

  <header>
    <h2>{exam.name}</h2>
    <p class="subtitle">{totalQuestions} domande disponibili</p>
  </header>

  <p class="label">Quante domande vuoi fare?</p>

  <div class="preset-grid">
    {#each presets.filter(n => n <= totalQuestions) as n}
      <button
        class="preset-btn"
        class:active={selected === n}
        on:click={() => { selected = n; custom = ''; }}
      >
        {n}
      </button>
    {/each}
    <button
      class="preset-btn"
      class:active={selected === 'all'}
      on:click={() => { selected = 'all'; custom = ''; }}
    >
      Tutte ({totalQuestions})
    </button>
  </div>

  <div class="custom-row">
    <label for="custom-count">Oppure inserisci un numero:</label>
    <input
      id="custom-count"
      type="number"
      min="1"
      max={totalQuestions}
      bind:value={custom}
      on:input={() => (selected = null)}
      placeholder="es. 15"
    />
  </div>

  <button
    class="start-btn"
    disabled={!count}
    on:click={start}
  >
    Inizia quiz →
  </button>
</div>

<style>
  .page {
    max-width: 500px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
  }

  .back-btn {
    background: none;
    border: none;
    color: var(--color-primary);
    font-size: 0.95rem;
    cursor: pointer;
    padding: 0.25rem 0;
    margin-bottom: 1.5rem;
  }

  header { margin-bottom: 2rem; }

  h2 { margin: 0 0 0.25rem; font-size: 1.5rem; }

  .subtitle { color: var(--color-muted); margin: 0; }

  .label {
    font-weight: 600;
    margin-bottom: 0.75rem;
  }

  .preset-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .preset-btn {
    padding: 0.6rem 1.25rem;
    border: 2px solid var(--color-border);
    border-radius: 8px;
    background: var(--color-card);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
  }

  .preset-btn.active,
  .preset-btn:hover {
    border-color: var(--color-primary);
    background: var(--color-card-hover);
  }

  .custom-row {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    margin-bottom: 2rem;
  }

  .custom-row label { font-size: 0.9rem; color: var(--color-muted); }

  .custom-row input {
    padding: 0.6rem 0.75rem;
    border: 2px solid var(--color-border);
    border-radius: 8px;
    font-size: 1rem;
    width: 100%;
    box-sizing: border-box;
    background: var(--color-card);
    color: inherit;
  }

  .custom-row input:focus {
    outline: none;
    border-color: var(--color-primary);
  }

  .start-btn {
    width: 100%;
    padding: 0.9rem;
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.15s;
  }

  .start-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .start-btn:not(:disabled):hover { opacity: 0.88; }
</style>
