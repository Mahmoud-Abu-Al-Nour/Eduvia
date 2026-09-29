import { Routes, Route } from 'react-router-dom'
import { HomePage } from '@/features/home/HomePage'
import { NotFoundPage } from '@/features/error/NotFoundPage'
import { LoginPage } from '@/features/auth/LoginPage'
import { ProtectedRoute } from '@/features/auth/ProtectedRoute'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { AdminDashboardPage } from '@/features/admin/AdminDashboardPage'
import { LearnerPortalPage } from '@/features/learner/LearnerPortalPage'
import { ActivityPlayer, InstructionalContentView } from '@/features/learning'
import { TeacherInstructionalContent } from '@/features/instructional'
import { ResearchWorkspacePage } from '@/features/research/ResearchWorkspacePage'

/**
 * Eduvia Application Shell
 *
 * Defines the top-level routing structure across four distinct role scopes:
 * - Admin: Platform-wide user management, platform analytics, global directory.
 * - Teacher: Classroom cohort, instructional content studio, practice activities, IEP reports.
 * - Learner: Dedicated learner portal, self progress, sensory preferences, practice player.
 * - Researcher: Research Mode sandbox, experiments, variants, prompt studio, comparative analysis.
 */
function App() {
  return (
    <>
      <a href="#main-content" className="skip-to-content">
        Skip to main content
      </a>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />

        {/* Learner Non-Evaluative Instructional Content View */}
        <Route path="/learn/objective/:objectiveId/content" element={<InstructionalContentView />} />

        {/* Learner Multi-Question Activity Player */}
        <Route path="/learn" element={<ActivityPlayer />} />
        <Route path="/learn/:activityId" element={<ActivityPlayer />} />

        {/* Learner Dedicated Portal */}
        <Route element={<ProtectedRoute allowedRoles={["learner", "teacher", "admin"]} />}>
          <Route path="/learner" element={<LearnerPortalPage />} />
          <Route path="/learner/journey" element={<LearnerPortalPage initialTab="journey" />} />
          <Route path="/learner/progress" element={<LearnerPortalPage initialTab="progress" />} />
          <Route path="/learner/preferences" element={<LearnerPortalPage initialTab="preferences" />} />
        </Route>

        {/* Admin Platform Workspace */}
        <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
          <Route path="/admin" element={<AdminDashboardPage />} />
          <Route path="/admin/overview" element={<AdminDashboardPage initialTab="overview" />} />
          <Route path="/admin/users" element={<AdminDashboardPage initialTab="users" />} />
          <Route path="/admin/learners" element={<AdminDashboardPage initialTab="learners" />} />
        </Route>

        {/* Teacher Classroom Workspace */}
        <Route element={<ProtectedRoute allowedRoles={["teacher", "admin"]} />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/teacher" element={<DashboardPage />} />
          <Route path="/teacher/dashboard" element={<DashboardPage />} />
          <Route path="/instructional" element={<DashboardPage initialTab="instructional" />} />
          <Route path="/curriculum" element={<DashboardPage initialTab="curriculum" />} />
          <Route path="/learners" element={<DashboardPage initialTab="learners" />} />
          <Route path="/learners/:id" element={<DashboardPage initialTab="learners" />} />
          <Route path="/analytics" element={<DashboardPage initialTab="analytics" />} />
          <Route path="/recommendations" element={<DashboardPage initialTab="recommendations" />} />
          <Route path="/teacher/instructional-content" element={<TeacherInstructionalContent />} />
          <Route path="/teacher/instructional-content/:contentId" element={<TeacherInstructionalContent />} />
        </Route>

        {/* Research Sandbox Workspace */}
        <Route element={<ProtectedRoute allowedRoles={["researcher", "admin"]} />}>
          <Route path="/research" element={<ResearchWorkspacePage />} />
          <Route path="/research/projects" element={<ResearchWorkspacePage initialTab="projects" />} />
          <Route path="/research/projects/:projectId" element={<ResearchWorkspacePage initialTab="projects" />} />
          <Route path="/research/projects/:projectId/experiments/:experimentId" element={<ResearchWorkspacePage initialTab="experiments" />} />
          <Route path="/research/prompt-studio" element={<ResearchWorkspacePage initialTab="studio" />} />
          <Route path="/research/compare" element={<ResearchWorkspacePage initialTab="compare" />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  )
}

export default App
