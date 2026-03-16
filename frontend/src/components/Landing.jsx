import './Landing.css'

export default function Landing({ onStart }) {
  return (
    <div className="landing">
      <div className="landing-content">
        <h1 className="landing-title">Smart Insurance Cost Estimator</h1>
        <p className="landing-subtitle">
          Get an AI-powered estimate of your health insurance premium based on your
          personal details, lifestyle, health conditions, and financial profile.
        </p>
        <button className="landing-cta" onClick={onStart}>
          Start Health Insurance Assessment
        </button>
        <div className="landing-features">
          <span>✓ ML-powered prediction</span>
          <span>✓ Risk assessment</span>
          <span>✓ Lifestyle suggestions</span>
        </div>
      </div>
    </div>
  )
}
