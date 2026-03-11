<script>
  export let exams = [];
  export let onSelect = () => {};

  let loading = true;
  let error = null;

  async function loadExams() {
    try {
      const res = await fetch('./exams.json');
      if (!res.ok) throw new Error('Impossibile caricare gli esami');
      exams = await res.json();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  loadExams();
</script>

<div class="page">
  <header>
    <h1>📚 Kela Quiz</h1>
    <p class="subtitle">Seleziona un esame per iniziare a esercitarti</p>
  </header>

  {#if loading}
    <p class="center muted">Caricamento esami...</p>
  {:else if error}
    <p class="center error">{error}</p>
  {:else}
    <div class="exam-grid">
      {#each exams as exam}
        <button class="exam-card" on:click={() => onSelect(exam)}>
          <span class="exam-icon">🎓</span>
          <span class="exam-name">{exam.name}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  header {
    text-align: center;
    margin-bottom: 2.5rem;
  }

  h1 {
    font-size: 2rem;
    margin: 0 0 0.5rem;
  }

  .subtitle {
    color: var(--color-muted);
    margin: 0;
  }

  .exam-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .exam-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    background: var(--color-card);
    border: 1.5px solid var(--color-border);
    border-radius: 14px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s, box-shadow 0.15s, transform 0.1s;
    text-align: left;
    width: 100%;
    box-shadow: 0 1px 4px var(--color-shadow);
    color: var(--color-text);
  }

  .exam-card:hover,
  .exam-card:focus-visible {
    border-color: var(--color-primary);
    background: var(--color-card-hover);
    box-shadow: 0 4px 12px var(--color-shadow);
    transform: translateY(-1px);
    outline: none;
  }

  .exam-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .center { text-align: center; }
  .muted { color: var(--color-muted); }
  .error { color: var(--color-wrong); }
</style>
