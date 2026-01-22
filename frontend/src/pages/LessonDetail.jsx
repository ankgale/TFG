import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  CheckCircle2, 
  XCircle, 
  ChevronRight,
  Zap,
  BookOpen
} from 'lucide-react';
import clsx from 'clsx';
import { lessonsApi } from '../services/api';
import translations from '../i18n/translations';

function LessonDetail() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const { lesson: lessonText, sampleLesson } = translations;
  
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState('content'); // 'content' | 'quiz' | 'complete'
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [earnedXp, setEarnedXp] = useState(0);

  useEffect(() => {
    async function fetchLesson() {
      try {
        const data = await lessonsApi.getLesson(lessonId);
        setLesson(data);
      } catch (error) {
        console.log('Using sample lesson:', error.message);
        setLesson(sampleLesson);
      } finally {
        setLoading(false);
      }
    }

    fetchLesson();
  }, [lessonId, sampleLesson]);

  const handleStartQuiz = () => {
    setCurrentStep('quiz');
    setCurrentQuizIndex(0);
    setCorrectAnswers(0);
    setEarnedXp(0);
  };

  const handleAnswerSelect = (optionId) => {
    if (showResult) return;
    setSelectedAnswer(optionId);
  };

  const handleSubmitAnswer = () => {
    if (!selectedAnswer) return;
    
    const currentQuiz = lesson.quizzes[currentQuizIndex];
    const selectedOption = currentQuiz.options.find(o => o.id === selectedAnswer);
    
    if (selectedOption?.is_correct) {
      setCorrectAnswers(prev => prev + 1);
      setEarnedXp(prev => prev + 10);
    }
    
    setShowResult(true);
  };

  const handleNextQuestion = () => {
    if (currentQuizIndex < lesson.quizzes.length - 1) {
      setCurrentQuizIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      // Quiz complete
      setEarnedXp(prev => prev + lesson.xp_reward);
      setCurrentStep('complete');
    }
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
          <div className="h-12 bg-gray-200 rounded w-3/4 mb-8" />
          <div className="space-y-4">
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-5/6" />
            <div className="h-4 bg-gray-200 rounded w-4/5" />
          </div>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-3xl mx-auto text-center py-12">
        <p className="text-gray-500">{lessonText.lessonNotFound}</p>
        <Link to="/" className="btn btn-primary mt-4">
          {lessonText.backToModules}
        </Link>
      </div>
    );
  }

  const currentQuiz = lesson.quizzes?.[currentQuizIndex];

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate(-1)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </button>
        <div className="flex-1">
          <p className="text-sm text-gray-500">{lessonText.title}</p>
          <h1 className="text-2xl font-bold text-gray-900">{lesson.title}</h1>
        </div>
        <div className="xp-badge">
          <Zap className="w-4 h-4" />
          +{lesson.xp_reward} XP
        </div>
      </div>

      {/* Progress indicator for quiz */}
      {currentStep === 'quiz' && (
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>{lessonText.question} {currentQuizIndex + 1} {lessonText.of} {lesson.quizzes.length}</span>
            <span>{correctAnswers} {lessonText.correct}</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${((currentQuizIndex + 1) / lesson.quizzes.length) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Content Step */}
      {currentStep === 'content' && (
        <div className="card">
          <div className="prose prose-lg max-w-none">
            {/* Simple markdown-like rendering */}
            {lesson.content.split('\n').map((line, i) => {
              if (line.startsWith('# ')) {
                return <h1 key={i} className="text-2xl font-bold mt-6 mb-4">{line.slice(2)}</h1>;
              }
              if (line.startsWith('## ')) {
                return <h2 key={i} className="text-xl font-bold mt-6 mb-3 text-gray-800">{line.slice(3)}</h2>;
              }
              if (line.startsWith('### ')) {
                return <h3 key={i} className="text-lg font-semibold mt-4 mb-2 text-gray-700">{line.slice(4)}</h3>;
              }
              if (line.startsWith('**') && line.endsWith('**')) {
                return <p key={i} className="font-bold">{line.slice(2, -2)}</p>;
              }
              if (line.match(/^\d\./)) {
                return <p key={i} className="ml-4 my-1">{line}</p>;
              }
              if (line.trim() === '') {
                return <br key={i} />;
              }
              return <p key={i} className="text-gray-700 my-2">{line}</p>;
            })}
          </div>

          <div className="mt-8 pt-6 border-t border-gray-100">
            <button
              onClick={handleStartQuiz}
              className="btn btn-primary w-full py-3"
            >
              <BookOpen className="w-5 h-5 mr-2" />
              {lessonText.startQuiz} ({lesson.quizzes?.length || 0} {lessonText.questions})
            </button>
          </div>
        </div>
      )}

      {/* Quiz Step */}
      {currentStep === 'quiz' && currentQuiz && (
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            {currentQuiz.question}
          </h2>

          <div className="space-y-3 mb-6">
            {currentQuiz.options.map((option) => {
              const isSelected = selectedAnswer === option.id;
              const isCorrect = option.is_correct;
              
              return (
                <button
                  key={option.id}
                  onClick={() => handleAnswerSelect(option.id)}
                  disabled={showResult}
                  className={clsx(
                    'w-full text-left p-4 rounded-xl border-2 transition-all',
                    !showResult && isSelected && 'border-primary-500 bg-primary-50',
                    !showResult && !isSelected && 'border-gray-200 hover:border-gray-300',
                    showResult && isCorrect && 'border-green-500 bg-green-50',
                    showResult && isSelected && !isCorrect && 'border-red-500 bg-red-50',
                    showResult && 'cursor-default'
                  )}
                >
                  <div className="flex items-center gap-3">
                    <div className={clsx(
                      'w-6 h-6 rounded-full border-2 flex items-center justify-center',
                      !showResult && isSelected && 'border-primary-500 bg-primary-500',
                      !showResult && !isSelected && 'border-gray-300',
                      showResult && isCorrect && 'border-green-500 bg-green-500',
                      showResult && isSelected && !isCorrect && 'border-red-500 bg-red-500'
                    )}>
                      {showResult && isCorrect && <CheckCircle2 className="w-4 h-4 text-white" />}
                      {showResult && isSelected && !isCorrect && <XCircle className="w-4 h-4 text-white" />}
                    </div>
                    <span className={clsx(
                      'font-medium',
                      showResult && isCorrect && 'text-green-700',
                      showResult && isSelected && !isCorrect && 'text-red-700'
                    )}>
                      {option.text}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Explanation */}
          {showResult && (
            <div className={clsx(
              'p-4 rounded-xl mb-6',
              currentQuiz.options.find(o => o.id === selectedAnswer)?.is_correct
                ? 'bg-green-50 border border-green-200'
                : 'bg-amber-50 border border-amber-200'
            )}>
              <p className="font-semibold mb-1">
                {currentQuiz.options.find(o => o.id === selectedAnswer)?.is_correct
                  ? `✓ ${lessonText.correctAnswer}`
                  : `✗ ${lessonText.incorrectAnswer}`}
              </p>
              <p className="text-sm text-gray-600">{currentQuiz.explanation}</p>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex gap-3">
            {!showResult ? (
              <button
                onClick={handleSubmitAnswer}
                disabled={!selectedAnswer}
                className="btn btn-primary flex-1 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {lessonText.checkAnswer}
              </button>
            ) : (
              <button
                onClick={handleNextQuestion}
                className="btn btn-primary flex-1 py-3"
              >
                {currentQuizIndex < lesson.quizzes.length - 1 ? (
                  <>
                    {lessonText.nextQuestion}
                    <ChevronRight className="w-5 h-5 ml-1" />
                  </>
                ) : (
                  lessonText.completeLesson
                )}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Complete Step */}
      {currentStep === 'complete' && (
        <div className="card text-center py-12">
          <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 className="w-10 h-10 text-primary-500" />
          </div>
          
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            {lessonText.lessonComplete}
          </h2>
          <p className="text-gray-600 mb-6">
            {lessonText.youAnswered} {correctAnswers} {lessonText.outOf} {lesson.quizzes.length} {lessonText.questionsCorrectly}
          </p>

          <div className="inline-flex items-center gap-2 bg-secondary-100 text-secondary-700 px-6 py-3 rounded-xl text-lg font-bold mb-8">
            <Zap className="w-6 h-6" />
            +{earnedXp} {lessonText.xpEarned}
          </div>

          <div className="flex gap-3 justify-center">
            <Link to="/" className="btn btn-outline">
              {lessonText.backToModules}
            </Link>
            <button 
              onClick={() => {
                setCurrentStep('content');
                setCurrentQuizIndex(0);
                setSelectedAnswer(null);
                setShowResult(false);
                setCorrectAnswers(0);
                setEarnedXp(0);
              }}
              className="btn btn-primary"
            >
              {lessonText.tryAgain}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default LessonDetail;
