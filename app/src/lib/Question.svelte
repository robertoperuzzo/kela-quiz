<script>
  export let question;       // { id, question, alternatives, correct }
  export let index;          // 0-based current question index
  export let total;          // total questions in session
  export let onNext = () => {};

  let selected = null;
  let answered = false;

  $: isCorrect = selected === question.correct;

  function choose(i) {
    if (answered) return;
    selected = i;
    answered = true;
  }

  function next() {
    onNext(isCorrect);
    selected = null;
    answered = false;
  }
</script>

<div class="page">
  <div class="progress-bar">
    <div class="progress-fill" style="width: {((index) / total) * 100}%"></div>
  </div>
  <p class="progress-label">Domanda {index + 1} di {total}</p>

  <div class="question-card">
    <p class="question-text">{question.question}</p>

    <div class="alternatives">
      {#each question.alternatives as alt, i}
        <button
          class="alt-btn"
          class:correct={answered && i === question.correct}
          class:wrong={answered && i === selected && i !== question.correct}
          disabled={answered}
          on:click={() => choose(i)}
        >
          <span class="alt-letter">{String.fromCharCode(65 + i)}</span>
          <span class="alt-text">{alt}</span>
        </button>
      {/each}
    </div>

    {#if answered}
      <div class="feedback" class:feedback-correct={isCorrect} class:feedback-wrong={!isCorrect}>
        {isCorrect ? '✅ Risposta corretta!' : '❌ Risposta sbagliata'}
      </div>
      <button class="next-btn" on:click={next}>
        {index + 1 < total ? 'Prossima →' : 'Vedi risultato →'}
      </button>
    {/if}
  </div>
</div>

<style>
  .page {
    max-width: 640px;
    margin: 0 auto;
    padding: 1.25rem 1rem;
  }

  .progress-bar {
    height: 6px;
    background: var(--color-border);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }

  .progress-fill {
    height: 100%;
    background: var(--color-primary);
    transition: width 0.3s;
  }

  .progress-label {
    text-align: right;
    font-size: 0.85rem;
    color: var(--color-muted);
    margin: 0 0 1.25rem;
  }

  .question-card {
    background: var(--color-card);
    border: 1.5px solid var(--color-border);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px var(--color-shadow);
  }

  .question-text {
    font-size: 1.1rem;
    font-weight: 600;
    line-height: 1.5;
    margin: 0 0 1.25rem;
  }

  .alternatives {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .alt-btn {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    width: 100%;
    padding: 0.85rem 1rem;
    background: var(--color-bg);
    border: 1.5px solid var(--color-border);
    border-radius: 10px;
    font-size: 0.97rem;
    text-align: left;
    cursor: pointer;
    transition: border-color 0.12s, background 0.12s, box-shadow 0.12s;
    line-height: 1.4;
    color: var(--color-text);
  }

  .alt-btn:not(:disabled):hover {
    border-color: var(--color-primary);
    background: var(--color-card-hover);
    box-shadow: 0 2px 6px var(--color-shadow);
  }

  .alt-btn.correct {
    border-color: var(--color-correct-border);
    background: var(--color-correct-bg);
    color: var(--color-text);
    border-left: 4px solid var(--color-correct);
  }

  .alt-btn.wrong {
    border-color: var(--color-wrong-border);
    background: var(--color-wrong-bg);
    color: var(--color-text);
    border-left: 4px solid var(--color-wrong);
  }

  .alt-btn:disabled { cursor: default; }

  .alt-letter {
    font-weight: 700;
    color: var(--color-primary);
    flex-shrink: 0;
    min-width: 1.2rem;
  }

  .alt-btn.correct .alt-letter { color: var(--color-correct); }
  .alt-btn.wrong .alt-letter { color: var(--color-wrong); }

  .feedback {
    margin-top: 1rem;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
  }

  .feedback-correct {
    background: var(--color-correct-bg);
    color: var(--color-correct);
    border: 1px solid var(--color-correct-border);
  }

  .feedback-wrong {
    background: var(--color-wrong-bg);
    color: var(--color-wrong);
    border: 1px solid var(--color-wrong-border);
  }

  .next-btn {
    margin-top: 1rem;
    width: 100%;
    padding: 0.8rem;
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.15s;
  }

  .next-btn:hover { opacity: 0.88; }
</style>
