/**
 * Translations for the FinLearn app.
 * All UI text is stored here for easy localization.
 * Code remains in English, only user-facing text is translated.
 */

const translations = {
  // App name and branding
  appName: 'FinLearn',

  // Navigation & Sidebar
  nav: {
    learningModules: 'Módulos de Aprendizaje',
    learningModulesDesc: 'Aprende conceptos financieros',
    stockSimulation: 'Simulador de Bolsa',
    stockSimulationDesc: 'Practica trading',
    achievements: 'Logros',
    modes: 'Modos',
  },

  // User stats
  user: {
    level: 'Nivel',
    xp: 'XP',
    toNextLevel: 'para el siguiente nivel',
    dayStreak: 'días de racha',
    student: 'Estudiante',
  },

  // Authentication
  auth: {
    login: 'Iniciar Sesión',
    register: 'Registrarse',
    logout: 'Cerrar Sesión',
    username: 'Nombre de usuario',
    email: 'Correo electrónico',
    password: 'Contraseña',
    confirmPassword: 'Confirmar contraseña',
    loginButton: 'Entrar',
    registerButton: 'Crear cuenta',
    noAccount: '¿No tienes cuenta?',
    hasAccount: '¿Ya tienes cuenta?',
    createAccount: 'Crear una cuenta',
    loginHere: 'Inicia sesión aquí',
    welcomeBack: '¡Bienvenido de nuevo!',
    createAccountTitle: 'Crea tu cuenta',
    loginSubtitle: 'Ingresa tus credenciales para continuar',
    registerSubtitle: 'Únete a FinLearn y comienza a aprender',
    invalidCredentials: 'Credenciales inválidas',
    passwordsDontMatch: 'Las contraseñas no coinciden',
    registrationSuccess: 'Cuenta creada exitosamente',
    passwordMinLength: 'La contraseña debe tener al menos 8 caracteres',
  },

  // Dashboard
  dashboard: {
    title: 'Módulos de Aprendizaje',
    modulesAvailable: 'Módulos Disponibles',
    totalLessons: 'Lecciones Totales',
    xpAvailable: 'XP Disponible',
    completed: 'Completados',
    dailyChallenge: 'Desafío Diario',
    dailyChallengeDesc: '¡Completa 3 lecciones hoy para ganar XP extra y mantener tu racha!',
    progress: 'Progreso',
    startLearning: 'Empezar a Aprender',
    moreModulesComingSoon: 'Más módulos próximamente. ¡Mantente atento para temas avanzados!',
  },

  // Module card
  module: {
    lessons: 'lecciones',
    progress: 'Progreso',
    moreLessons: 'lecciones más',
    difficulty: {
      beginner: 'Principiante',
      intermediate: 'Intermedio',
      advanced: 'Avanzado',
    },
  },

  // Lesson
  lesson: {
    title: 'Lección',
    startQuiz: 'Comenzar Cuestionario',
    questions: 'preguntas',
    question: 'Pregunta',
    of: 'de',
    correct: 'correctas',
    checkAnswer: 'Comprobar Respuesta',
    nextQuestion: 'Siguiente Pregunta',
    completeLesson: 'Completar Lección',
    lessonComplete: '¡Lección Completada!',
    youAnswered: 'Respondiste',
    outOf: 'de',
    questionsCorrectly: 'preguntas correctamente',
    xpEarned: '¡XP Ganados!',
    backToModules: 'Volver a Módulos',
    tryAgain: 'Intentar de Nuevo',
    correctAnswer: '¡Correcto!',
    incorrectAnswer: 'No del todo correcto',
    lessonNotFound: 'Lección no encontrada',
  },

  // Stock simulation
  stocks: {
    title: 'Simulador del Mercado de Valores',
    live: 'En Vivo',
    offline: 'Desconectado',
    refresh: 'Actualizar',
    cashBalance: 'Saldo en Efectivo',
    portfolioValue: 'Valor del Portafolio',
    totalGainLoss: 'Ganancia/Pérdida Total',
    holdings: 'Posiciones',
    stocks: 'Acciones',
    selectStock: 'Selecciona una acción',
    selectStockDesc: 'Haz clic en cualquier acción de la lista para ver su gráfico y operar',
    today: 'hoy',
    buy: 'Comprar',
    sell: 'Vender',
    paperTradingMode: 'Modo de Trading Virtual',
    paperTradingDesc: 'Esta es una simulación con dinero virtual. No se realizan transacciones reales. Los precios de las acciones son solo con fines educativos.',
    numberOfShares: 'Número de Acciones',
    enterAmount: 'Ingresa la cantidad',
    estimatedTotal: 'Total Estimado',
    availableBalance: 'Saldo Disponible',
    cancel: 'Cancelar',
    confirmBuy: 'Confirmar Compra',
    confirmSell: 'Confirmar Venta',
  },

  // Chart periods
  periods: {
    '1d': '1D',
    '5d': '5D',
    '1mo': '1M',
    '3mo': '3M',
    '1y': '1A',
  },

  // Sample modules (Spanish content)
  sampleModules: [
    {
      id: 1,
      title: 'Introducción a la Inversión',
      description: 'Aprende los fundamentos de la inversión, incluyendo acciones, bonos y fondos mutuos. Perfecto para principiantes que comienzan su camino financiero.',
      icon: '📈',
      color: '#6366f1',
      difficulty: 'beginner',
      xp_reward: 500,
      lessons_count: 5,
      lessons: [
        { id: 1, title: '¿Qué es Invertir?', xp_reward: 50 },
        { id: 2, title: 'Tipos de Inversiones', xp_reward: 50 },
        { id: 3, title: 'Riesgo y Rentabilidad', xp_reward: 50 },
        { id: 4, title: 'Construyendo un Portafolio', xp_reward: 50 },
        { id: 5, title: 'Primeros Pasos', xp_reward: 50 },
      ],
    },
    {
      id: 2,
      title: 'Fundamentos del Mercado de Valores',
      description: 'Comprende cómo funciona el mercado de valores, desde los índices bursátiles hasta la mecánica del trading. Conocimiento esencial para cualquier inversor.',
      icon: '📊',
      color: '#10b981',
      difficulty: 'beginner',
      xp_reward: 600,
      lessons_count: 6,
      lessons: [
        { id: 6, title: 'Cómo Funcionan los Mercados', xp_reward: 50 },
        { id: 7, title: 'Leyendo Cotizaciones', xp_reward: 50 },
        { id: 8, title: 'Órdenes de Mercado vs Límite', xp_reward: 50 },
        { id: 9, title: 'Entendiendo los Índices', xp_reward: 50 },
        { id: 10, title: 'Mercados Alcistas y Bajistas', xp_reward: 50 },
        { id: 11, title: 'Horarios de Trading', xp_reward: 50 },
      ],
    },
    {
      id: 3,
      title: 'Finanzas Personales Básicas',
      description: 'Domina los conceptos básicos de finanzas personales incluyendo presupuesto, ahorro y gestión de deudas de manera efectiva.',
      icon: '💰',
      color: '#f59e0b',
      difficulty: 'beginner',
      xp_reward: 450,
      lessons_count: 4,
      lessons: [
        { id: 12, title: 'Creando un Presupuesto', xp_reward: 50 },
        { id: 13, title: 'Fondo de Emergencia', xp_reward: 50 },
        { id: 14, title: 'Gestión de Deudas', xp_reward: 50 },
        { id: 15, title: 'Estrategias de Ahorro', xp_reward: 50 },
      ],
    },
    {
      id: 4,
      title: 'Análisis Técnico',
      description: 'Aprende a leer gráficos, identificar patrones y usar indicadores técnicos para tomar decisiones de trading informadas.',
      icon: '📉',
      color: '#8b5cf6',
      difficulty: 'intermediate',
      xp_reward: 800,
      lessons_count: 8,
      lessons: [
        { id: 16, title: 'Introducción a los Gráficos', xp_reward: 50 },
        { id: 17, title: 'Soporte y Resistencia', xp_reward: 50 },
        { id: 18, title: 'Medias Móviles', xp_reward: 50 },
      ],
    },
  ],

  // Sample lesson content
  sampleLesson: {
    id: 1,
    title: '¿Qué es Invertir?',
    description: 'Aprende los conceptos fundamentales de la inversión y por qué es importante para tu futuro financiero.',
    content: `
# ¿Qué es Invertir?

Invertir es el acto de asignar dinero o recursos con la expectativa de generar ingresos o ganancias a lo largo del tiempo. A diferencia del ahorro, donde simplemente guardas dinero, invertir pone tu dinero a trabajar.

## ¿Por qué Invertir?

1. **Superar la Inflación**: Tu dinero pierde valor con el tiempo debido a la inflación. Invertir ayuda a que tu patrimonio crezca más rápido que la inflación.

2. **Construir Riqueza**: A través del poder del interés compuesto, incluso pequeñas inversiones pueden crecer significativamente con el tiempo.

3. **Alcanzar Metas**: Ya sea la jubilación, comprar una casa o financiar la educación, invertir puede ayudarte a alcanzar tus objetivos financieros.

## Conceptos Clave

### Riesgo y Rentabilidad
Generalmente, mayores rendimientos potenciales vienen con mayor riesgo. Entender tu tolerancia al riesgo es crucial.

### Diversificación
No pongas todos los huevos en la misma cesta. Distribuir las inversiones entre diferentes activos reduce el riesgo.

### Horizonte Temporal
Cuanto más tiempo puedas dejar tu dinero invertido, más tiempo tendrá para crecer y recuperarse de las fluctuaciones del mercado.
    `,
    xp_reward: 50,
    estimated_time: 5,
    quizzes: [
      {
        id: 1,
        question: '¿Cuál es la principal diferencia entre ahorrar e invertir?',
        options: [
          { id: 1, text: 'Ahorrar implica poner dinero en un banco, invertir no', is_correct: false },
          { id: 2, text: 'Invertir pone tu dinero a trabajar para generar rendimientos', is_correct: true },
          { id: 3, text: 'No hay diferencia', is_correct: false },
          { id: 4, text: 'Ahorrar es más arriesgado que invertir', is_correct: false },
        ],
        explanation: 'Mientras que ahorrar típicamente significa guardar dinero en cuentas seguras, invertir implica asignar dinero en activos que pueden potencialmente crecer en valor con el tiempo.',
      },
      {
        id: 2,
        question: '¿Qué es la diversificación?',
        options: [
          { id: 5, text: 'Invertir todo tu dinero en una sola acción', is_correct: false },
          { id: 6, text: 'Distribuir inversiones entre diferentes activos para reducir el riesgo', is_correct: true },
          { id: 7, text: 'Solo invertir en empresas de tecnología', is_correct: false },
          { id: 8, text: 'Mantener todo tu dinero en efectivo', is_correct: false },
        ],
        explanation: 'La diversificación significa distribuir tus inversiones entre varios tipos de activos, sectores y regiones geográficas para reducir el riesgo.',
      },
      {
        id: 3,
        question: '¿Por qué es importante el horizonte temporal en la inversión?',
        options: [
          { id: 9, text: 'Determina cuándo abre el mercado de valores', is_correct: false },
          { id: 10, text: 'Horizontes más largos permiten más tiempo de recuperación ante fluctuaciones del mercado', is_correct: true },
          { id: 11, text: 'Solo importa para traders diarios', is_correct: false },
          { id: 12, text: 'El horizonte temporal no tiene impacto en la inversión', is_correct: false },
        ],
        explanation: 'Un horizonte temporal más largo le da a tus inversiones más tiempo para crecer a través del interés compuesto y recuperarse de caídas temporales del mercado.',
      },
    ],
  },

  // Common
  common: {
    loading: 'Cargando...',
    error: 'Error',
    save: 'Guardar',
    delete: 'Eliminar',
    edit: 'Editar',
    close: 'Cerrar',
    confirm: 'Confirmar',
    back: 'Volver',
  },
};

export default translations;

// Helper function to get nested translation
export function t(key) {
  const keys = key.split('.');
  let value = translations;
  
  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = value[k];
    } else {
      console.warn(`Translation not found: ${key}`);
      return key;
    }
  }
  
  return value;
}
