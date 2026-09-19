import React, { useState } from "react";
import { useAuth } from "@/features/auth/AuthContext";
import { BookOpen, Users, BarChart3, LogOut } from "lucide-react";
import { CurriculumBrowser } from "@/features/curriculum/CurriculumBrowser";
import { LearnerManager } from "@/features/learners/LearnerManager";

interface DashboardPageProps {
  initialTab?: string;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ initialTab = "overview" }) => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState(initialTab);

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-gray-200">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
            <span className="text-white font-bold text-xl">E</span>
          </div>
          <span className="text-xl font-bold text-gray-900">Eduvia</span>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1">
          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("overview"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'overview' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <BarChart3 className={`w-5 h-5 mr-3 ${activeTab === 'overview' ? 'text-blue-700' : 'text-gray-400'}`} />
            Overview
          </a>
          
          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("curriculum"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'curriculum' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <BookOpen className={`w-5 h-5 mr-3 ${activeTab === 'curriculum' ? 'text-blue-700' : 'text-gray-400'}`} />
            Curriculum
          </a>

          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("learners"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'learners' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <Users className={`w-5 h-5 mr-3 ${activeTab === 'learners' ? 'text-blue-700' : 'text-gray-400'}`} />
            Learners
          </a>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center mb-4 px-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold mr-3">
              {user?.full_name?.charAt(0) || user?.email.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{user?.full_name || "Teacher"}</p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
          </div>
          
          <button
            onClick={logout}
            className="flex w-full items-center px-3 py-2 text-sm font-medium text-red-600 rounded-lg hover:bg-red-50 transition-colors"
          >
            <LogOut className="w-5 h-5 mr-3 text-red-500" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
          <h1 className="text-xl font-semibold text-gray-900 capitalize">{activeTab}</h1>
        </header>
        
        <div className="flex-1 p-8 overflow-auto">
          {activeTab === "overview" && (
            <div className="max-w-4xl">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Welcome back!</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="text-sm font-medium text-gray-500 mb-1">Active Learners</div>
                  <div className="text-3xl font-bold text-gray-900">0</div>
                </div>
                
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="text-sm font-medium text-gray-500 mb-1">Pending Activities</div>
                  <div className="text-3xl font-bold text-gray-900">0</div>
                </div>
                
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="text-sm font-medium text-gray-500 mb-1">Alerts</div>
                  <div className="text-3xl font-bold text-gray-900">0</div>
                </div>
              </div>
            </div>
          )}
          
          {activeTab === "curriculum" && (
            <div className="max-w-6xl">
              <CurriculumBrowser />
            </div>
          )}
          
          {activeTab === "learners" && (
            <div className="max-w-6xl">
              <LearnerManager />
            </div>
          )}
        </div>
      </main>
    </div>
  );
};
