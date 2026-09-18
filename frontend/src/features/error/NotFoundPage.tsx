/**
 * 404 Not Found Page
 */
import { motion } from 'framer-motion'
import { Brain, Home } from 'lucide-react'
import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50/30 flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center max-w-md"
      >
        <div className="w-20 h-20 rounded-3xl gradient-brand flex items-center justify-center mx-auto mb-6 shadow-lg">
          <Brain className="w-10 h-10 text-white" aria-hidden="true" />
        </div>
        <h1 className="font-display text-6xl font-bold text-gray-200 mb-4" aria-label="404 Not Found">
          404
        </h1>
        <p className="text-xl font-semibold text-gray-900 mb-2">Page not found</p>
        <p className="text-gray-500 mb-8">
          This page hasn't been built yet. Eduvia is currently in Phase 0.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl gradient-brand text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-200 focus-visible:ring-2 focus-visible:ring-brand-500"
          id="back-home-btn"
        >
          <Home className="w-4 h-4" aria-hidden="true" />
          Back to Home
        </Link>
      </motion.div>
    </div>
  )
}
