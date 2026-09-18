/**
 * Eduvia Home Page — Phase 0 Initialization Showcase
 *
 * Displays the Eduvia platform overview and system connectivity status.
 * This page will be replaced by the Teacher Dashboard in Phase 10.
 *
 * Accessibility requirements met:
 * - Single h1 per page
 * - Semantic HTML structure
 * - Sufficient color contrast
 * - Keyboard navigable
 * - Focus-visible styles
 */
import { motion } from 'framer-motion'
import {
  BookOpen,
  Brain,
  CheckCircle2,
  ChevronRight,
  Database,
  Heart,
  RefreshCw,
  Server,
  Sparkles,
  Users,
  XCircle,
  Zap,
} from 'lucide-react'
import { useHealth } from '@/hooks/useHealth'
import { cn } from '@/utils/cn'

const FEATURES = [
  {
    icon: BookOpen,
    title: 'Structured Curriculum',
    description:
      'Same learning objectives delivered through personalized methods — visual, audio, interactive, and more.',
    color: 'text-brand-500',
    bg: 'bg-brand-50',
  },
  {
    icon: Brain,
    title: 'Adaptive Intelligence',
    description:
      'Evidence-based learner profiling tracks what works — without permanent labels or medical diagnoses.',
    color: 'text-purple-500',
    bg: 'bg-purple-50',
  },
  {
    icon: Users,
    title: 'Teacher-Led',
    description:
      'Teachers remain the decision makers. AI provides recommendations — never autonomous diagnoses.',
    color: 'text-accent-500',
    bg: 'bg-accent-50',
  },
  {
    icon: Heart,
    title: 'Accessibility First',
    description:
      'Large touch targets, clear typography, reduced motion support, and high contrast for all learners.',
    color: 'text-rose-500',
    bg: 'bg-rose-50',
  },
  {
    icon: Zap,
    title: '5 Activity Types',
    description:
      'Matching, Multiple Choice, Ordering, Visual Identification, and Drag & Drop — all schema-driven.',
    color: 'text-amber-500',
    bg: 'bg-amber-50',
  },
  {
    icon: Sparkles,
    title: 'RAG-Powered Generation',
    description:
      'Gemini generates activities guided by a real educational knowledge base — not free-form invention.',
    color: 'text-emerald-500',
    bg: 'bg-emerald-50',
  },
]

const PHASES = [
  { phase: '0', name: 'Initialization', status: 'current' },
  { phase: '1', name: 'Auth & Database', status: 'upcoming' },
  { phase: '2', name: 'Curriculum', status: 'upcoming' },
  { phase: '3', name: 'Learner Profiles', status: 'upcoming' },
  { phase: '4', name: 'Activity Engine', status: 'upcoming' },
  { phase: '5', name: 'Learner Experience', status: 'upcoming' },
  { phase: '6', name: 'Performance Tracking', status: 'upcoming' },
  { phase: '7', name: 'Learning Analytics', status: 'upcoming' },
  { phase: '8', name: 'Adaptive Engine', status: 'upcoming' },
  { phase: '9', name: 'Gemini + RAG', status: 'upcoming' },
]

// ── Animation Variants ────────────────────────────────────────────────────

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
}

// ── Sub-Components ────────────────────────────────────────────────────────

function StatusBadge({
  healthy,
  label,
}: {
  healthy: boolean | null | undefined
  label: string
}) {
  if (healthy === null || healthy === undefined) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-400">
        <div className="w-2 h-2 rounded-full bg-gray-300 animate-pulse" />
        <span>{label}</span>
      </div>
    )
  }
  return (
    <div
      className={cn(
        'flex items-center gap-2 text-sm font-medium',
        healthy ? 'text-emerald-600' : 'text-red-500',
      )}
      role="status"
      aria-label={`${label}: ${healthy ? 'connected' : 'unavailable'}`}
    >
      {healthy ? (
        <CheckCircle2 className="w-4 h-4" aria-hidden="true" />
      ) : (
        <XCircle className="w-4 h-4" aria-hidden="true" />
      )}
      <span>{label}</span>
    </div>
  )
}

function SystemStatusPanel() {
  const { health, isLoading, error, refresh } = useHealth()

  return (
    <motion.div
      variants={itemVariants}
      className="rounded-2xl border border-gray-200 bg-white shadow-sm overflow-hidden"
      aria-labelledby="system-status-heading"
    >
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Server className="w-5 h-5 text-gray-500" aria-hidden="true" />
          <h2 id="system-status-heading" className="font-semibold text-gray-800">
            System Status
          </h2>
        </div>
        <button
          onClick={refresh}
          disabled={isLoading}
          className={cn(
            'p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100',
            'transition-colors focus-visible:ring-2 focus-visible:ring-brand-500',
            'disabled:opacity-50',
          )}
          aria-label="Refresh system status"
          id="refresh-status-btn"
        >
          <RefreshCw
            className={cn('w-4 h-4', isLoading && 'animate-spin')}
            aria-hidden="true"
          />
        </button>
      </div>

      <div className="p-6 space-y-3">
        {error ? (
          <div
            className="text-sm text-red-600 bg-red-50 rounded-lg p-3"
            role="alert"
          >
            <strong>Backend unreachable:</strong> {error}
            <p className="mt-1 text-xs text-red-500">
              Make sure the backend is running on localhost:8000
            </p>
          </div>
        ) : (
          <>
            <StatusBadge
              healthy={health ? true : null}
              label="Backend API"
            />
            <StatusBadge
              healthy={health?.dependencies?.database?.healthy}
              label="PostgreSQL"
            />
            <StatusBadge
              healthy={health?.dependencies?.qdrant?.healthy}
              label="Qdrant"
            />
            <StatusBadge
              healthy={health?.dependencies?.ai_provider?.configured}
              label="Gemini AI"
            />
          </>
        )}

        {health && (
          <div className="pt-3 border-t border-gray-100">
            <p className="text-xs text-gray-400">
              API v{health.version} · Uptime {Math.round((health.uptime_seconds ?? 0) / 60)}m
            </p>
          </div>
        )}
      </div>
    </motion.div>
  )
}

// ── Main Component ────────────────────────────────────────────────────────

export function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
      {/* Skip to main content — accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-brand-600 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg"
      >
        Skip to main content
      </a>

      {/* ── Header ────────────────────────────────────────────────────── */}
      <header className="border-b border-gray-200/60 bg-white/70 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-xl gradient-brand flex items-center justify-center shadow-sm"
              aria-hidden="true"
            >
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="font-display font-bold text-gray-900 text-xl">Eduvia</span>
            <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-brand-100 text-brand-700">
              Phase 0
            </span>
          </div>
          <nav aria-label="Primary navigation">
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                'text-sm text-gray-500 hover:text-gray-800 transition-colors',
                'flex items-center gap-1',
              )}
              id="api-docs-link"
            >
              API Docs <ChevronRight className="w-3 h-3" aria-hidden="true" />
            </a>
          </nav>
        </div>
      </header>

      {/* ── Main Content ───────────────────────────────────────────────── */}
      <main id="main-content">
        {/* Hero Section */}
        <section
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16"
          aria-labelledby="hero-heading"
        >
          <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            className="text-center max-w-4xl mx-auto"
          >
            <motion.div variants={itemVariants} className="mb-6">
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-100 text-brand-700 text-sm font-medium">
                <Sparkles className="w-4 h-4" aria-hidden="true" />
                Adaptive Educational Platform — MVP Initialization
              </span>
            </motion.div>

            <motion.h1
              variants={itemVariants}
              className="font-display text-5xl sm:text-6xl font-bold text-gray-900 mb-6 leading-tight"
              id="hero-heading"
            >
              Standardized Curriculum,{' '}
              <span className="gradient-text">Personalized Delivery</span>
            </motion.h1>

            <motion.p
              variants={itemVariants}
              className="text-xl text-gray-600 mb-8 leading-relaxed max-w-3xl mx-auto"
            >
              Eduvia helps teachers deliver the same learning objectives through different
              teaching approaches — adapting to each learner's observed patterns without
              permanent labels or medical diagnoses.
            </motion.p>

            <motion.div
              variants={itemVariants}
              className="flex flex-col sm:flex-row gap-3 justify-center"
            >
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className={cn(
                  'inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl',
                  'gradient-brand text-white font-semibold shadow-lg shadow-brand-500/25',
                  'hover:shadow-xl hover:shadow-brand-500/30 hover:-translate-y-0.5',
                  'transition-all duration-200 focus-visible:ring-2 focus-visible:ring-brand-500',
                )}
                id="explore-api-btn"
              >
                <Zap className="w-4 h-4" aria-hidden="true" />
                Explore API
              </a>
              <a
                href="https://github.com"
                className={cn(
                  'inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl',
                  'border border-gray-200 bg-white text-gray-700 font-semibold',
                  'hover:bg-gray-50 hover:border-gray-300 transition-all duration-200',
                  'focus-visible:ring-2 focus-visible:ring-brand-500',
                )}
                id="view-docs-btn"
              >
                <BookOpen className="w-4 h-4" aria-hidden="true" />
                Documentation
              </a>
            </motion.div>
          </motion.div>
        </section>

        {/* Core Loop Diagram */}
        <section
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16"
          aria-labelledby="loop-heading"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="rounded-3xl bg-gradient-to-r from-brand-600 to-indigo-700 p-8 sm:p-12 text-white overflow-hidden relative"
          >
            <div
              className="absolute inset-0 opacity-10"
              aria-hidden="true"
              style={{
                backgroundImage:
                  'radial-gradient(circle at 20% 50%, white 1px, transparent 1px), radial-gradient(circle at 80% 20%, white 1px, transparent 1px)',
                backgroundSize: '40px 40px',
              }}
            />
            <h2
              id="loop-heading"
              className="font-display text-2xl sm:text-3xl font-bold mb-8 text-center"
            >
              The Eduvia Learning Loop
            </h2>
            <div className="flex flex-wrap justify-center gap-2 sm:gap-4 relative z-10">
              {[
                'Curriculum',
                'Learning Objective',
                'Learner Profile',
                'Strategy Selection',
                'Activity Generation',
                'Learner Interaction',
                'Performance Tracking',
                'Learning Analytics',
                'Learner Profile Update',
              ].map((step, i) => (
                <div key={step} className="flex items-center gap-2">
                  <div className="px-3 py-2 rounded-xl bg-white/15 backdrop-blur-sm text-sm font-medium text-white border border-white/20 whitespace-nowrap">
                    {step}
                  </div>
                  {i < 8 && (
                    <ChevronRight
                      className="w-4 h-4 text-white/50 flex-shrink-0"
                      aria-hidden="true"
                    />
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* Features Grid */}
        <section
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16"
          aria-labelledby="features-heading"
        >
          <h2
            id="features-heading"
            className="font-display text-3xl font-bold text-gray-900 text-center mb-12"
          >
            Platform Capabilities
          </h2>
          <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {FEATURES.map((feature) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  variants={itemVariants}
                  className={cn(
                    'p-6 rounded-2xl border border-gray-100 bg-white shadow-sm',
                    'hover:shadow-md hover:-translate-y-1 transition-all duration-200',
                  )}
                >
                  <div
                    className={cn(
                      'w-12 h-12 rounded-xl flex items-center justify-center mb-4',
                      feature.bg,
                    )}
                    aria-hidden="true"
                  >
                    <Icon className={cn('w-6 h-6', feature.color)} />
                  </div>
                  <h3 className="font-display font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-gray-500 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              )
            })}
          </motion.div>
        </section>

        {/* System Status + Development Roadmap */}
        <section
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20"
          aria-labelledby="status-heading"
        >
          <h2
            id="status-heading"
            className="font-display text-3xl font-bold text-gray-900 text-center mb-12"
          >
            Development Status
          </h2>
          <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            className="grid grid-cols-1 lg:grid-cols-3 gap-6"
          >
            {/* System connectivity */}
            <div className="lg:col-span-1">
              <SystemStatusPanel />
            </div>

            {/* Development roadmap */}
            <motion.div
              variants={itemVariants}
              className="lg:col-span-2 rounded-2xl border border-gray-200 bg-white shadow-sm overflow-hidden"
              aria-labelledby="roadmap-heading"
            >
              <div className="px-6 py-4 border-b border-gray-100 flex items-center gap-2">
                <Database className="w-5 h-5 text-gray-500" aria-hidden="true" />
                <h3 id="roadmap-heading" className="font-semibold text-gray-800">
                  Development Roadmap
                </h3>
              </div>
              <div className="p-6">
                <ol className="space-y-3" aria-label="Development phases">
                  {PHASES.map((p) => (
                    <li key={p.phase} className="flex items-center gap-3">
                      <div
                        className={cn(
                          'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0',
                          p.status === 'current'
                            ? 'gradient-brand text-white shadow-md'
                            : 'bg-gray-100 text-gray-400',
                        )}
                        aria-label={`Phase ${p.phase}`}
                      >
                        {p.phase}
                      </div>
                      <span
                        className={cn(
                          'text-sm',
                          p.status === 'current'
                            ? 'font-semibold text-gray-900'
                            : 'text-gray-500',
                        )}
                      >
                        {p.name}
                        {p.status === 'current' && (
                          <span
                            className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700"
                            aria-label="Currently in progress"
                          >
                            ✓ Complete
                          </span>
                        )}
                      </span>
                    </li>
                  ))}
                </ol>
              </div>
            </motion.div>
          </motion.div>
        </section>
      </main>

      {/* ── Footer ────────────────────────────────────────────────────── */}
      <footer className="border-t border-gray-200 bg-white/70 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-brand-500" aria-hidden="true" />
            <span className="font-display font-semibold text-gray-900">Eduvia</span>
            <span className="text-gray-400 text-sm">Phase 0 — Initialization</span>
          </div>
          <p className="text-sm text-gray-400 text-center">
            This system does not diagnose medical or psychological conditions.
            Teachers remain the decision makers.
          </p>
        </div>
      </footer>
    </div>
  )
}
