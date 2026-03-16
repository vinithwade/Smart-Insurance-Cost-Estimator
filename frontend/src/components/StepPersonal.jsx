export default function StepPersonal({ form, updateForm, nextStep, prevStep }) {
  const bmi = form.height && form.weight
    ? (form.weight / ((form.height / 100) ** 2)).toFixed(1)
    : null

  return (
    <>
      <h2 className="step-title">Personal Information</h2>
      <div className="form-group">
        <label>Age</label>
        <input
          type="number"
          min="18"
          max="100"
          placeholder="24"
          value={form.age}
          onChange={(e) => updateForm({ age: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Gender</label>
        <select
          value={form.gender}
          onChange={(e) => updateForm({ gender: e.target.value })}
        >
          <option value="">Select</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>
      <div className="form-group">
        <label>Height (cm)</label>
        <input
          type="number"
          min="100"
          max="250"
          placeholder="170"
          value={form.height}
          onChange={(e) => updateForm({ height: e.target.value })}
        />
      </div>
      <div className="form-group">
        <label>Weight (kg)</label>
        <input
          type="number"
          min="30"
          max="300"
          placeholder="70"
          value={form.weight}
          onChange={(e) => updateForm({ weight: e.target.value })}
        />
        {bmi && (
          <span className="bmi-hint">BMI: {bmi}</span>
        )}
      </div>
      <div className="form-group">
        <label>Number of Dependents</label>
        <input
          type="number"
          min="0"
          max="20"
          placeholder="2"
          value={form.dependents}
          onChange={(e) => updateForm({ dependents: e.target.value })}
        />
      </div>
      <div className="form-actions">
        <button className="btn btn-secondary" onClick={prevStep} disabled>
          Back
        </button>
        <button
          className="btn btn-primary"
          onClick={nextStep}
          disabled={!form.age || !form.gender || !form.height || !form.weight}
        >
          Next
        </button>
      </div>
    </>
  )
}
