import React from 'react'
import { Link } from 'react-router-dom'
import {
  CheckCircle2,
  ChevronRight,
  ShieldCheck,
  HeartHandshake,
  Layers,
  ArrowRight,
  Eye,
  ListOrdered,
  MoveRight,
  MousePointerClick,
  Compass,
  FileCheck2,
} from 'lucide-react'
import { useHealth } from '@/hooks/useHealth'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

const CORE_LOOP_STEPS = [
  {
    step: '01',
    title: 'Standard Curriculum',
    description: 'Shared, structured curriculum benchmarks aligned with national and regional educational standards.',
    highlight: 'Unified Goals',
  },
  {
    step: '02',
    title: 'Same Learning Objective',
    description: 'Every learner targets the exact same educational milestone — no watered-down expectations.',
    highlight: 'High Expectations',
  },
  {
    step: '03',
    title: 'Differentiated Delivery',
    description: 'Content adapts dynamically across visual, interactive, audial, and kinesthetic presentation modes.',
    highlight: 'Tailored Approach',
  },
  {
    step: '04',
    title: 'Evidence-Based Tracking',
    description: 'Records concrete response latency, assistance levels, and accuracy without diagnostic labeling.',
    highlight: 'Objective Data',
  },
  {
    step: '05',
    title: 'Teacher-Led Adaptation',
    description: 'Empirical learning patterns inform teacher recommendations for subsequent targeted practice.',
    highlight: 'Teacher In Control',
  },
]

const MODALITIES = [
  {
    icon: Eye,
    title: 'Visual Identification',
    description: 'Targeted visual mapping with gentle auditory reinforcement for early symbol and quantity recognition.',
    badge: 'Foundational',
  },
  {
    icon: MousePointerClick,
    title: 'Scaffolded Choice',
    description: 'Multiple-choice prompts with graduated hint ladders that preserve confidence while measuring independent mastery.',
    badge: 'Formative',
  },
  {
    icon: Layers,
    title: 'Matching & Associations',
    description: 'Multi-sensory association connecting abstract numerical digits to concrete real-world quantities.',
    badge: 'Concept Link',
  },
  {
    icon: ListOrdered,
    title: 'Progressive Ordering',
    description: 'Sequential ordering tasks designed with high touch targets and immediate, gentle auditory validation.',
    badge: 'Sequence',
  },
  {
    icon: MoveRight,
    title: 'Tactile Drag & Drop',
    description: 'Kinesthetic grouping activities calibrated for touchscreens, switches, and assistive pointer devices.',
    badge: 'Kinesthetic',
  },
]

export const HomePage: React.FC = () => {
  const { health, isLoading: healthLoading } = useHealth()

  return (
    <div className="min-h-screen bg-[#faf8f5] text-slate-900 selection:bg-teal-100 selection:text-teal-900">
      {/* ── Top Navigation Bar ────────────────────────────────────────────── */}
      <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-brand-800 text-white flex items-center justify-center font-bold text-lg shadow-xs">
              E
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight text-slate-900 block leading-tight">Eduvia</span>
              <span className="text-[11px] font-medium text-slate-500 block leading-none">Adaptive Learning Platform</span>
            </div>
          </div>

          <div className="flex items-center gap-3 sm:gap-4">
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 text-xs font-medium text-slate-600">
              <span className={`w-2 h-2 rounded-full ${health?.status === 'ok' ? 'bg-emerald-500' : 'bg-amber-400'}`} />
              <span>{healthLoading ? 'Checking system...' : health?.status === 'ok' ? 'Platform Operational' : 'Dev Mode Active'}</span>
            </div>
            <Link to="/login">
              <Button variant="default" size="sm" className="font-semibold shadow-xs">
                Teacher Portal
                <ArrowRight className="w-4 h-4 ml-1.5" />
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* ── Hero Section ─────────────────────────────────────────────────── */}
      <section className="relative pt-12 pb-16 md:pt-20 md:pb-24 overflow-hidden border-b border-slate-200/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            <Badge variant="secondary" className="px-3 py-1 text-xs font-semibold tracking-wide uppercase">
              Educational Support System
            </Badge>

            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-slate-900 leading-[1.15]">
              Standardized Curriculum.{' '}
              <span className="text-brand-800 block sm:inline">Personalized Delivery.</span>
            </h1>

            <p className="text-lg sm:text-xl text-slate-600 leading-relaxed font-normal">
              Eduvia supports learners with intellectual disabilities and special educational needs to reach the{' '}
              <strong className="text-slate-900 font-semibold">same learning objectives</strong> through{' '}
              <strong className="text-slate-900 font-semibold">diverse, adapted activity modalities</strong> based on empirical learning evidence.
            </p>

            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3.5">
              <Link to="/login" className="w-full sm:w-auto">
                <Button size="lg" className="w-full sm:w-auto font-semibold">
                  Launch Teacher Workspace
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
              <a href="#how-it-works" className="w-full sm:w-auto">
                <Button variant="outline" size="lg" className="w-full sm:w-auto font-semibold">
                  How The Educational Loop Works
                </Button>
              </a>
            </div>

            <div className="pt-6 flex flex-wrap items-center justify-center gap-6 text-xs text-slate-500 font-medium">
              <div className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Zero Diagnostic Labels</span>
              </div>
              <div className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Teachers Always In Control</span>
              </div>
              <div className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>WCAG AAA Accessible</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Core Educational Principle (The Learning Loop) ───────────────── */}
      <section id="how-it-works" className="py-16 md:py-24 bg-white border-b border-slate-200/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center space-y-3 mb-12 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              The Eduvia Educational Loop
            </h2>
            <p className="text-slate-600 text-base leading-relaxed">
              Standardized learning objectives remain constant; the delivery method flexes to each learner&apos;s cognitive and sensory strengths.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 lg:gap-6 relative">
            {CORE_LOOP_STEPS.map((item, index) => (
              <div
                key={item.step}
                className="relative rounded-2xl border border-slate-200/90 bg-[#fbfaf8] p-5 flex flex-col justify-between transition-all hover:border-brand-300 hover:shadow-xs"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold font-mono text-brand-800 bg-brand-50 px-2 py-0.5 rounded-md border border-brand-200/60">
                      STEP {item.step}
                    </span>
                    <Badge variant="outline" className="text-[10px]">
                      {item.highlight}
                    </Badge>
                  </div>
                  <h3 className="font-semibold text-base text-slate-900 tracking-tight">
                    {item.title}
                  </h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {item.description}
                  </p>
                </div>

                {index < CORE_LOOP_STEPS.length - 1 && (
                  <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 z-10">
                    <div className="w-6 h-6 rounded-full bg-white border border-slate-300 shadow-2xs flex items-center justify-center text-slate-400">
                      <ChevronRight className="w-3.5 h-3.5" />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 5 Schema-Driven Learning Modalities ───────────────────────────── */}
      <section className="py-16 md:py-24 bg-[#faf8f5] border-b border-slate-200/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center space-y-3 mb-12 sm:mb-16">
            <Badge variant="secondary" className="px-3 py-1 text-xs font-semibold">
              Flexible Pedagogy
            </Badge>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              5 Schema-Driven Activity Modalities
            </h2>
            <p className="text-slate-600 text-base leading-relaxed">
              Every curriculum objective can be generated into any of these five validated formats, ensuring learners engage in their optimal processing mode.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {MODALITIES.map((mod) => {
              const Icon = mod.icon
              return (
                <Card key={mod.title} className="bg-white border-slate-200 hover:border-brand-200">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between mb-2">
                      <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-800 flex items-center justify-center">
                        <Icon className="w-5 h-5" />
                      </div>
                      <Badge variant="secondary">{mod.badge}</Badge>
                    </div>
                    <CardTitle className="text-base font-semibold">{mod.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {mod.description}
                    </p>
                  </CardContent>
                </Card>
              )
            })}

            {/* IEP Summary Card */}
            <Card className="bg-gradient-to-br from-brand-900 to-brand-950 text-white border-none sm:col-span-2 lg:col-span-1 flex flex-col justify-between">
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-10 h-10 rounded-xl bg-white/10 text-white flex items-center justify-center">
                    <FileCheck2 className="w-5 h-5 text-amber-300" />
                  </div>
                  <Badge variant="outline" className="text-white border-white/30 text-[10px]">
                    IEP Aligned
                  </Badge>
                </div>
                <CardTitle className="text-base font-semibold text-white">
                  Individualized Education Plans
                </CardTitle>
                <p className="text-xs text-slate-300 leading-relaxed pt-2">
                  Generates rigorous IEP progress reports tracking objective mastery, assistance trends, and effective accommodations with 1-click export.
                </p>
              </CardHeader>
              <div className="p-6 pt-0">
                <Link to="/login">
                  <Button variant="accent" size="sm" className="w-full font-semibold">
                    Explore In Teacher Portal
                    <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                  </Button>
                </Link>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* ── Teacher Governance & Ethics ──────────────────────────────────── */}
      <section className="py-16 md:py-20 bg-white border-b border-slate-200/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="space-y-4">
              <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-800 flex items-center justify-center">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">
                Teacher as Decision Maker
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Adaptive algorithms propose recommendations and generate tailored exercises, but educators always maintain veto and adjustment rights.
              </p>
            </div>

            <div className="space-y-4">
              <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-800 flex items-center justify-center">
                <HeartHandshake className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">
                No Diagnostic Labeling
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Eduvia is not a medical diagnostic tool. We track what concrete instructional accommodations work best — never affixing permanent clinical classifications.
              </p>
            </div>

            <div className="space-y-4">
              <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-800 flex items-center justify-center">
                <Compass className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">
                Accessible by Design
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Built from the ground up to support screen readers, switches, touch interfaces with 44×44px minimum targets, and reduced cognitive visual clutter.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── Footer ──────────────────────────────────────────────────────── */}
      <footer className="py-10 bg-slate-900 text-slate-400 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white text-sm">Eduvia</span>
            <span>—</span>
            <span>Adaptive Educational Platform for Special Needs Support</span>
          </div>

          <div className="flex items-center gap-6">
            <Link to="/login" className="hover:text-white transition-colors">
              Teacher Login
            </Link>
            <span className="text-slate-600">|</span>
            <span>Version 0.1.0</span>
          </div>
        </div>
      </footer>
    </div>
  )
}
