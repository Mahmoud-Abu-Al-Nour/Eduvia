import { Routes, Route } from 'react-router-dom'
import { HomePage } from '@/features/home/HomePage'
import { NotFoundPage } from '@/features/error/NotFoundPage'
import { LoginPage } from '@/features/auth/LoginPage'
import { ProtectedRoute } from '@/features/auth/ProtectedRoute'
import { DashboardPage } from '@/features/dashboard/DashboardPage'

/**
 * Eduvia Application Shell
 *
 * Defines the top-level routing structure.
 * Feature areas are lazy-loaded as they are developed (Phase 1+).
 *
 * Route structure (future phases):
 * /                    → Landing / Dashboard
 * /login               → Auth (Phase 1)
 * /dashboard           → Teacher/Admin dashboard (Phase 10)
 * /learners            → Learner management (Phase 3)
 * /learners/:id        → Learner profile (Phase 3)
 * /curriculum          → Curriculum management (Phase 2)
 * /activities          → Activity management (Phase 4)
 * /learn/:sessionId    → Learner activity interface (Phase 5)
 * /analytics           → Learning analytics (Phase 7)
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      
      <Route element={<ProtectedRoute allowedRoles={["admin", "teacher"]} />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/curriculum" element={<DashboardPage initialTab="curriculum" />} />
        <Route path="/learners" element={<DashboardPage initialTab="learners" />} />
        <Route path="/learners/:id" element={<DashboardPage initialTab="learners" />} />
      </Route>
      
      {/* Future routes will be added here as phases are implemented */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default App
