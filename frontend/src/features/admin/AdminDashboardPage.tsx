import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthContext";
import api from "@/services/api";
import type { Learner, PlatformStats, User, UserRole } from "@/types";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  ShieldCheck,
  Users,
  GraduationCap,
  LogOut,
  UserCheck,
  PlusCircle,
  Search,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Layers,
  ArrowRight,
  FlaskConical,
} from "lucide-react";

interface AdminDashboardPageProps {
  initialTab?: string;
}

export const AdminDashboardPage: React.FC<AdminDashboardPageProps> = ({ initialTab = "overview" }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(initialTab);

  // Platform Stats State
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(false);

  // Users State
  const [users, setUsers] = useState<User[]>([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [userRoleFilter, setUserRoleFilter] = useState<string>("all");
  const [userSearchQuery, setUserSearchQuery] = useState("");

  // Global Learners State
  const [allLearners, setAllLearners] = useState<Learner[]>([]);
  const [loadingLearners, setLoadingLearners] = useState(false);

  // Create User Modal State
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [newName, setNewName] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [newRole, setNewRole] = useState<UserRole>("teacher");
  const [createError, setCreateError] = useState("");
  const [creatingUser, setCreatingUser] = useState(false);

  // Fetch Platform Stats
  const fetchStats = async () => {
    try {
      setLoadingStats(true);
      const res = await api.get<PlatformStats>("/users/platform/stats");
      setStats(res);
    } catch (err) {
      console.error("Failed to load platform stats:", err);
      // Fallback stats if in offline/demo mode
      setStats({
        total_users: 5,
        total_admins: 1,
        total_teachers: 2,
        total_learners: 2,
        total_curricula: 1,
        total_activities_completed: 15,
      });
    } finally {
      setLoadingStats(false);
    }
  };

  // Fetch Users
  const fetchUsers = async () => {
    try {
      setLoadingUsers(true);
      const url = userRoleFilter !== "all" ? `/users/?role=${userRoleFilter}` : "/users/";
      const res = await api.get<User[]>(url);
      setUsers(res);
    } catch (err) {
      console.error("Failed to load users:", err);
    } finally {
      setLoadingUsers(false);
    }
  };

  // Fetch All Learners
  const fetchAllLearners = async () => {
    try {
      setLoadingLearners(true);
      const res = await api.get<Learner[]>("/learners");
      setAllLearners(res);
    } catch (err) {
      console.error("Failed to load platform learners:", err);
    } finally {
      setLoadingLearners(false);
    }
  };

  useEffect(() => {
    void fetchStats();
  }, []);

  useEffect(() => {
    if (activeTab === "users") {
      void fetchUsers();
    } else if (activeTab === "learners") {
      void fetchAllLearners();
    }
  }, [activeTab, userRoleFilter]);

  // Handle Role Change
  const handleRoleChange = async (userId: string, targetRole: UserRole) => {
    try {
      await api.patch(`/users/${userId}`, { role: targetRole });
      await fetchUsers();
      await fetchStats();
    } catch (err) {
      console.error("Failed to update user role:", err);
    }
  };

  // Handle Active Status Toggle
  const handleToggleActive = async (userId: string, currentActive: boolean) => {
    try {
      await api.patch(`/users/${userId}`, { is_active: !currentActive });
      await fetchUsers();
    } catch (err) {
      console.error("Failed to toggle user status:", err);
    }
  };

  // Handle Create User
  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreateError("");
    setCreatingUser(true);
    try {
      await api.post("/users/", {
        email: newEmail,
        full_name: newName,
        password: newPassword,
        role: newRole,
        is_active: true,
      });
      setShowCreateModal(false);
      setNewEmail("");
      setNewName("");
      setNewPassword("");
      await fetchUsers();
      await fetchStats();
    } catch (err: any) {
      setCreateError(err.message || "Failed to create user account.");
    } finally {
      setCreatingUser(false);
    }
  };

  const filteredUsers = users.filter((u) => {
    const matchesSearch =
      u.full_name.toLowerCase().includes(userSearchQuery.toLowerCase()) ||
      u.email.toLowerCase().includes(userSearchQuery.toLowerCase());
    return matchesSearch;
  });

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Top Admin Navigation Header */}
      <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-30 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/" className="flex items-center gap-2">
              <img src="/logo.jpg" alt="Eduvia" className="h-9 w-auto rounded object-contain bg-white p-0.5" />
              <span className="font-bold text-lg tracking-tight text-white">Eduvia</span>
            </Link>
            <div className="flex items-center gap-1.5 bg-brand-600/30 text-brand-300 border border-brand-500/40 px-2.5 py-0.5 rounded-full text-xs font-semibold">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Platform Administration</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-xs font-medium text-slate-200">{user?.full_name || "Platform Admin"}</p>
              <p className="text-[10px] text-slate-400 font-mono">{user?.email}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => logout()}
              className="text-slate-300 border-slate-700 hover:bg-slate-800 hover:text-white text-xs gap-1.5"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Admin Tab Bar */}
      <nav className="bg-white border-b border-slate-200 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex items-center space-x-1 sm:space-x-4 py-2 overflow-x-auto">
          <button
            onClick={() => setActiveTab("overview")}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all ${
              activeTab === "overview"
                ? "bg-slate-900 text-white shadow-2xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Platform Overview</span>
          </button>

          <button
            onClick={() => setActiveTab("users")}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all ${
              activeTab === "users"
                ? "bg-slate-900 text-white shadow-2xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Users className="w-4 h-4" />
            <span>User Management</span>
          </button>

          <button
            onClick={() => setActiveTab("learners")}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all ${
              activeTab === "learners"
                ? "bg-slate-900 text-white shadow-2xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <GraduationCap className="w-4 h-4" />
            <span>Global Learners Roster</span>
          </button>

          <button
            onClick={() => navigate("/dashboard")}
            className="px-3 py-2 rounded-md text-xs sm:text-sm font-semibold text-slate-500 hover:text-brand-700 hover:bg-brand-50 flex items-center gap-1.5 ml-auto"
            title="Inspect Teacher Dashboard View"
          >
            <span>Teacher Workspace</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => navigate("/research")}
            className="px-3 py-2 rounded-md text-xs sm:text-sm font-semibold text-purple-700 hover:text-purple-900 hover:bg-purple-50 flex items-center gap-1.5"
            title="Inspect Research Mode Sandbox"
          >
            <FlaskConical className="w-3.5 h-3.5" />
            <span>Research Mode</span>
          </button>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl mx-auto w-full p-4 sm:p-6 lg:p-8">
        {/* OVERVIEW TAB */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Platform Command Center</h1>
                <p className="text-xs sm:text-sm text-slate-600">
                  Global monitoring of educational assets, multi-tenant roles, and telemetry services.
                </p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={fetchStats}
                disabled={loadingStats}
                className="gap-1.5 text-xs self-start sm:self-auto"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${loadingStats ? "animate-spin" : ""}`} />
                <span>Refresh KPIs</span>
              </Button>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="border-slate-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-semibold text-slate-500 uppercase">
                    Total Users
                  </CardDescription>
                  <CardTitle className="text-2xl font-bold text-slate-900">
                    {stats?.total_users ?? 0}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-[11px] text-slate-500 flex gap-2">
                    <span>Admins: {stats?.total_admins ?? 0}</span>
                    <span>•</span>
                    <span>Teachers: {stats?.total_teachers ?? 0}</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-slate-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-semibold text-slate-500 uppercase">
                    Total Learners
                  </CardDescription>
                  <CardTitle className="text-2xl font-bold text-brand-700">
                    {stats?.total_learners ?? 0}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-[11px] text-slate-500">Registered across all classrooms</p>
                </CardContent>
              </Card>

              <Card className="border-slate-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-semibold text-slate-500 uppercase">
                    Active Curricula
                  </CardDescription>
                  <CardTitle className="text-2xl font-bold text-slate-900">
                    {stats?.total_curricula ?? 0}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-[11px] text-slate-500">Ministry of Education Standard</p>
                </CardContent>
              </Card>

              <Card className="border-slate-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-semibold text-slate-500 uppercase">
                    Evaluated Activities
                  </CardDescription>
                  <CardTitle className="text-2xl font-bold text-emerald-700">
                    {stats?.total_activities_completed ?? 0}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-[11px] text-slate-500">Authoritative telemetry events</p>
                </CardContent>
              </Card>
            </div>

            {/* Architecture Scope Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="border-slate-200 bg-slate-900 text-white">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge className="bg-amber-500/20 text-amber-300 border-amber-500/30">Admin Scope</Badge>
                    <ShieldCheck className="w-5 h-5 text-amber-400" />
                  </div>
                  <CardTitle className="text-base font-bold mt-2">Platform-Wide Oversight</CardTitle>
                </CardHeader>
                <CardContent className="text-xs text-slate-300 space-y-1.5">
                  <p>• Global user management &amp; role allocation</p>
                  <p>• Cross-cohort visibility across all learners</p>
                  <p>• Standardized curriculum authoring &amp; audit</p>
                  <p>• System health and rate limiter configurations</p>
                </CardContent>
              </Card>

              <Card className="border-slate-200">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">Teacher Scope</Badge>
                    <UserCheck className="w-5 h-5 text-blue-600" />
                  </div>
                  <CardTitle className="text-base font-bold mt-2">Assigned Cohort Authority</CardTitle>
                </CardHeader>
                <CardContent className="text-xs text-slate-600 space-y-1.5">
                  <p>• Dedicated to assigned learners only (IDOR safe)</p>
                  <p>• Instructional explanation generation &amp; publishing</p>
                  <p>• Multi-question practice activity studio</p>
                  <p>• IEP progress reporting &amp; intervention alerts</p>
                </CardContent>
              </Card>

              <Card className="border-slate-200">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200">Learner Scope</Badge>
                    <GraduationCap className="w-5 h-5 text-emerald-600" />
                  </div>
                  <CardTitle className="text-base font-bold mt-2">Personal Learner Experience</CardTitle>
                </CardHeader>
                <CardContent className="text-xs text-slate-600 space-y-1.5">
                  <p>• Self-only access to progress and mastery</p>
                  <p>• Published instructional explanations with TTS</p>
                  <p>• Accessible practice player with instant feedback</p>
                  <p>• Private teacher notes &amp; answer keys withheld</p>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* USER MANAGEMENT TAB */}
        {activeTab === "users" && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">User Management &amp; RBAC</h1>
                <p className="text-xs sm:text-sm text-slate-600">
                  Manage accounts, reassign roles, and configure platform access permissions.
                </p>
              </div>
              <Button
                onClick={() => setShowCreateModal(true)}
                className="gap-2 text-xs font-semibold self-start sm:self-auto bg-slate-900 hover:bg-slate-800 text-white"
              >
                <PlusCircle className="w-4 h-4" />
                <span>Create New User</span>
              </Button>
            </div>

            {/* Filter and Search Bar */}
            <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-white p-3 rounded-lg border border-slate-200">
              <div className="relative w-full sm:w-72">
                <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                <Input
                  placeholder="Search by name or email..."
                  value={userSearchQuery}
                  onChange={(e) => setUserSearchQuery(e.target.value)}
                  className="pl-9 text-xs"
                />
              </div>

              <div className="flex items-center gap-2 w-full sm:w-auto">
                <span className="text-xs text-slate-500 font-medium">Filter Role:</span>
                <select
                  value={userRoleFilter}
                  onChange={(e) => setUserRoleFilter(e.target.value)}
                  className="text-xs border border-slate-300 rounded px-2.5 py-1.5 bg-white text-slate-700 font-medium focus:outline-hidden focus:ring-1 focus:ring-slate-900"
                >
                  <option value="all">All Roles</option>
                  <option value="admin">Admin</option>
                  <option value="teacher">Teacher</option>
                  <option value="learner">Learner</option>
                  <option value="researcher">Researcher</option>
                </select>
                <Button variant="ghost" size="sm" onClick={fetchUsers} className="text-xs">
                  <RefreshCw className={`w-3.5 h-3.5 ${loadingUsers ? "animate-spin" : ""}`} />
                </Button>
              </div>
            </div>

            {/* Users Table */}
            <div className="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-2xs">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">
                  <tr>
                    <th className="py-3 px-4">User</th>
                    <th className="py-3 px-4">Role</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4">Registered</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredUsers.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-slate-400">
                        {loadingUsers ? "Loading user accounts..." : "No user accounts match current criteria."}
                      </td>
                    </tr>
                  ) : (
                    filteredUsers.map((u) => (
                      <tr key={u.id} className="hover:bg-slate-50/70 transition-colors">
                        <td className="py-3 px-4">
                          <p className="font-semibold text-slate-900">{u.full_name}</p>
                          <p className="text-[11px] text-slate-500 font-mono">{u.email}</p>
                        </td>
                        <td className="py-3 px-4">
                          {u.role === "admin" && (
                            <Badge className="bg-amber-100 text-amber-800 border-amber-200 font-semibold">
                              Admin
                            </Badge>
                          )}
                          {u.role === "teacher" && (
                            <Badge className="bg-blue-100 text-blue-800 border-blue-200 font-semibold">
                              Teacher
                            </Badge>
                          )}
                          {u.role === "learner" && (
                            <Badge className="bg-emerald-100 text-emerald-800 border-emerald-200 font-semibold">
                              Learner
                            </Badge>
                          )}
                          {u.role === "researcher" && (
                            <Badge className="bg-purple-100 text-purple-800 border-purple-200 font-semibold">
                              Researcher
                            </Badge>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          {u.is_active ? (
                            <span className="inline-flex items-center text-emerald-700 text-[11px] font-medium gap-1">
                              <CheckCircle2 className="w-3.5 h-3.5" /> Active
                            </span>
                          ) : (
                            <span className="inline-flex items-center text-rose-600 text-[11px] font-medium gap-1">
                              <AlertTriangle className="w-3.5 h-3.5" /> Suspended
                            </span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-slate-400 text-[11px]">
                          {new Date(u.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="inline-flex items-center gap-1.5">
                            {/* Role change dropdown */}
                            <select
                              value={u.role}
                              onChange={(e) => handleRoleChange(u.id, e.target.value as UserRole)}
                              disabled={u.id === user?.id} // Don't let admin demote self
                              className="text-[11px] border border-slate-200 rounded px-1.5 py-0.5 bg-white text-slate-700"
                            >
                              <option value="admin">Admin</option>
                              <option value="teacher">Teacher</option>
                              <option value="learner">Learner</option>
                              <option value="researcher">Researcher</option>
                            </select>

                            {/* Toggle Active status */}
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleToggleActive(u.id, u.is_active)}
                              disabled={u.id === user?.id}
                              className={`h-7 px-2 text-[11px] ${
                                u.is_active ? "text-rose-600 hover:text-rose-700" : "text-emerald-600 hover:text-emerald-700"
                              }`}
                            >
                              {u.is_active ? "Suspend" : "Activate"}
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* GLOBAL LEARNERS ROSTER TAB */}
        {activeTab === "learners" && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Global Learners Directory</h1>
                <p className="text-xs sm:text-sm text-slate-600">
                  Platform-wide oversight of enrolled students across all teacher cohorts.
                </p>
              </div>
              <Button variant="outline" size="sm" onClick={fetchAllLearners} className="gap-1.5 text-xs">
                <RefreshCw className={`w-3.5 h-3.5 ${loadingLearners ? "animate-spin" : ""}`} />
                <span>Refresh Directory</span>
              </Button>
            </div>

            <div className="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-2xs">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">
                  <tr>
                    <th className="py-3 px-4">Learner Name</th>
                    <th className="py-3 px-4">Educational Level</th>
                    <th className="py-3 px-4">Age Group</th>
                    <th className="py-3 px-4">Assigned Teacher</th>
                    <th className="py-3 px-4">User Account</th>
                    <th className="py-3 px-4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {allLearners.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="py-8 text-center text-slate-400">
                        {loadingLearners ? "Loading directory..." : "No learners found on the platform."}
                      </td>
                    </tr>
                  ) : (
                    allLearners.map((l) => (
                      <tr key={l.id} className="hover:bg-slate-50/70">
                        <td className="py-3 px-4 font-semibold text-slate-900">{l.name}</td>
                        <td className="py-3 px-4 capitalize">{l.learning_level}</td>
                        <td className="py-3 px-4 capitalize">{l.age_group}</td>
                        <td className="py-3 px-4">
                          {l.teacher_id ? (
                            <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                              Teacher Assigned
                            </Badge>
                          ) : (
                            <span className="text-slate-400 italic">Unassigned</span>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          {l.user_id ? (
                            <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200">
                              Linked Account
                            </Badge>
                          ) : (
                            <span className="text-slate-400 italic">No User Linked</span>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          {l.is_active ? (
                            <span className="text-emerald-700 font-medium">Active</span>
                          ) : (
                            <span className="text-rose-600 font-medium">Inactive</span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Create User Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 border border-slate-200">
            <h2 className="text-lg font-bold text-slate-900 mb-1">Create User Account</h2>
            <p className="text-xs text-slate-500 mb-4">
              Add a new account with platform credentials and specific role assignment.
            </p>

            {createError && (
              <div className="bg-rose-50 text-rose-700 p-2.5 rounded text-xs mb-3 border border-rose-200">
                {createError}
              </div>
            )}

            <form onSubmit={handleCreateUser} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                <Input
                  required
                  placeholder="e.g. Fatima Zahra"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                <Input
                  required
                  type="email"
                  placeholder="fatima@eduvia.app"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                <Input
                  required
                  type="password"
                  minLength={8}
                  placeholder="Minimum 8 characters"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Role Assignment</label>
                <select
                  value={newRole}
                  onChange={(e) => setNewRole(e.target.value as UserRole)}
                  className="w-full text-xs border border-slate-300 rounded px-3 py-2 bg-white text-slate-800 focus:outline-hidden focus:ring-1 focus:ring-slate-900"
                >
                  <option value="teacher">Teacher (Classroom &amp; Activities)</option>
                  <option value="learner">Learner (Practice &amp; Personal Profile)</option>
                  <option value="researcher">Researcher (Research Sandbox &amp; Experiments)</option>
                  <option value="admin">Administrator (Platform Management)</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setShowCreateModal(false)}
                  className="text-xs"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  size="sm"
                  isLoading={creatingUser}
                  className="bg-slate-900 text-white text-xs font-semibold"
                >
                  Save User
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
