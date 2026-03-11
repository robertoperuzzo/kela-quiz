<script>
  import ExamSelect from './lib/ExamSelect.svelte';
  import QuizSetup from './lib/QuizSetup.svelte';
  import Question from './lib/Question.svelte';
  import Score from './lib/Score.svelte';
  import { pickRandom, shuffleQuestion } from './lib/shuffle.js';

  // States: 'select' | 'setup' | 'quiz' | 'score'
  let state = 'select';

  let selectedExam = null;
  let allQuestions = [];
  let sessionQuestions = [];
  let questionCount = 0;
  let currentIndex = 0;
  let score = 0;
  let loading = false;
  let loadError = null;

  async function handleExamSelect(exam) {
    selectedExam = exam;
    loading = true;
    loadError = null;
    try {
      const res = await fetch(`./data/${exam.key}.json`);
      if (!res.ok) throw new Error(`Impossibile caricare le domande per ${exam.name}`);
      const data = await res.json();
      allQuestions = data.questions ?? [];
      state = 'setup';
    } catch (e) {
      loadError = e.message;
    } finally {
      loading = false;
    }
  }

  function handleStart(count) {
    questionCount = count;
    const picked = pickRandom(allQuestions, count);
    sessionQuestions = picked.map(shuffleQuestion);
    currentIndex = 0;
    score = 0;
    state = 'quiz';
  }

  function handleNext(wasCorrect) {
    if (wasCorrect) score += 1;
    if (currentIndex + 1 >= sessionQuestions.length) {
      state = 'score';
    } else {
      currentIndex += 1;
    }
  }

  function handleRetry() {
    handleStart(questionCount);
  }

  function handleBackToExams() {
    state = 'select';
    selectedExam = null;
    allQuestions = [];
    sessionQuestions = [];
  }
</script>

<main>
  {#if loading}
    <div class="center-page">
      <p class="muted">Caricamento domande...</p>
    </div>
  {:else if loadError}
    <div class="center-page">
      <p class="error">{loadError}</p>
      <button class="link-btn" on:click={() => { state = 'select'; loadError = null; }}>← Torna indietro</button>
    </div>
  {:else if state === 'select'}
    <ExamSelect onSelect={handleExamSelect} />
  {:else if state === 'setup'}
    <QuizSetup
      exam={selectedExam}
      totalQuestions={allQuestions.length}
      onStart={handleStart}
      onBack={handleBackToExams}
    />
  {:else if state === 'quiz'}
    <Question
      question={sessionQuestions[currentIndex]}
      index={currentIndex}
      total={sessionQuestions.length}
      onNext={handleNext}
    />
  {:else if state === 'score'}
    <Score
      {score}
      total={sessionQuestions.length}
      examName={selectedExam.name}
      onRetry={handleRetry}
      onBack={handleBackToExams}
    />
  {/if}
</main>

<style>
  main {
    min-height: 100vh;
    padding: 1rem 0 4rem;
  }

  .center-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    gap: 1rem;
  }

  .muted { color: var(--color-muted); }
  .error { color: var(--color-wrong); font-weight: 600; }

  .link-btn {
    background: none;
    border: none;
    color: var(--color-primary);
    font-size: 1rem;
    cursor: pointer;
  }
</style>
