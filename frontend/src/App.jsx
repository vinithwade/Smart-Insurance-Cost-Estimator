import { useState } from 'react'
import Landing from './components/Landing'
import StepPersonal from './components/StepPersonal'
import StepLifestyle from './components/StepLifestyle'
import StepHealth from './components/StepHealth'
import StepFinancial from './components/StepFinancial'
import Results from './components/Results'
import './App.css'

const STEPS = [
  { id: 1, title: 'Personal', component: StepPersonal },
  { id: 2, title: 'Lifestyle', component: StepLifestyle },
  { id: 3, title: 'Health', component: StepHealth },
  { id: 4, title: 'Financial', component: StepFinancial },
]

const INITIAL_FORM = {
  age: '',
  gender: '',
  height: '',
  weight: '',
  maritalStatus: 'single',
  dependents: '0',
  smoker: 'no',
  alcohol: 'occasionally',
  exercise: 'weekly',
  diet: 'mixed',
  diabetes: 'no',
  heartProblems: 'no',
  chronicDisease: 'no',
  income: '',
  savings: '',
  occupation: 'employed',
}

function App() {
  const [started, setStarted] = useState(false)
  const [step, setStep] = useState(1)
  const [form, setForm] = useState(INITIAL_FORM)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const updateForm = (updates) => {
    setForm((prev) => ({ ...prev, ...updates }))
  }

  const nextStep = () => {
    if (step < 4) setStep((s) => s + 1)
  }

  const prevStep = () => {
    if (step > 1) setStep((s) => s - 1)
  }

  const submitForm = async () => {
    setLoading(true)
    setError(null)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || ''
      const res = await fetch(`${apiUrl}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: parseInt(form.age, 10),
          gender: form.gender,
          height: parseFloat(form.height),
          weight: parseFloat(form.weight),
          marital_status: form.maritalStatus,
          dependents: parseInt(form.dependents, 10),
          smoker: form.smoker,
          alcohol: form.alcohol,
          exercise: form.exercise,
          diet: form.diet,
          diabetes: form.diabetes,
          heart_problems: form.heartProblems,
          chronic_disease: form.chronicDisease,
          income: parseInt(form.income, 10) || 500000,
          savings: parseInt(form.savings, 10) || 100000,
          occupation: form.occupation,
        }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || res.statusText)
      }
      const data = await res.json()
      setResult(data)
      setStep(5)
    } catch (err) {
      setError(err.message || 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setStarted(false)
    setStep(1)
    setForm(INITIAL_FORM)
    setResult(null)
    setError(null)
  }

  if (!started) {
    return <Landing onStart={() => setStarted(true)} />
  }

  if (step === 5 && result) {
    return <Results data={result} form={form} onReset={reset} />
  }

  const StepComponent = STEPS.find((s) => s.id === step)?.component
  if (!StepComponent) return null

  return (
    <div className="app-form">
      <header className="form-header">
        <h1>Health Insurance Assessment</h1>
        <div className="step-indicator">
          {STEPS.map((s) => (
            <span
              key={s.id}
              className={`step-dot ${s.id <= step ? 'active' : ''}`}
            >
              {s.id}
            </span>
          ))}
        </div>
      </header>

      <main className="form-content">
        <StepComponent
          form={form}
          updateForm={updateForm}
          nextStep={nextStep}
          prevStep={prevStep}
          submitForm={submitForm}
          isLast={step === 4}
          loading={loading}
          error={error}
        />
      </main>
    </div>
  )
}

export default App
