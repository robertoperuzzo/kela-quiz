/**
 * Fisher-Yates shuffle — returns a new shuffled array, does not mutate original.
 */
export function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Shuffle the alternatives of a question while keeping track of the correct answer.
 * Returns a new question object with shuffled alternatives and updated correct index.
 */
export function shuffleQuestion(question) {
  const indices = shuffle([0, 1, 2, 3].slice(0, question.alternatives.length));
  const newAlternatives = indices.map(i => question.alternatives[i]);
  const newCorrect = indices.indexOf(question.correct);
  return { ...question, alternatives: newAlternatives, correct: newCorrect };
}

/**
 * Pick `count` random items from an array (without repetition).
 * If count >= arr.length, returns a shuffled copy of the full array.
 */
export function pickRandom(arr, count) {
  const shuffled = shuffle(arr);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}
