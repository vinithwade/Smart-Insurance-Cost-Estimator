export default function StepLifestyle({ form, updateForm, nextStep, prevStep }) {
  return (
    <>
      <h2 className="step-title">Lifestyle Habits</h2>
      <div className="form-group">
        <label>Do you smoke?</label>
        <select
          value={form.smoker}
          onChange={(e) => updateForm({ smoker: e.target.value })}
        >
          <option value="no">No</option>
          <option value="yes">Yes</option>
        </select>
      </div>
      <div className="form-group">
        <label>Do you drink alcohol?</label>
        <select
          value={form.alcohol}
          onChange={(e) => updateForm({ alcohol: e.target.value })}
        >
          <option value="never">Never</option>
          <option value="occasionally">Occasionally</option>
          <option value="often">Often</option>
        </select>
      </div>
      <div className="form-group">
        <label>How often do you exercise?</label>
        <select
          value={form.exercise}
          onChange={(e) => updateForm({ exercise: e.target.value })}
        >
          <option value="none">None</option>
          <option value="weekly">Weekly</option>
          <option value="daily">Daily</option>
        </select>
      </div>
      <div className="form-group">
        <label>What type of diet do you follow?</label>
        <select
          value={form.diet}
          onChange={(e) => updateForm({ diet: e.target.value })}
        >
          <option value="veg">Veg</option>
          <option value="non-veg">Non-veg</option>
          <option value="mixed">Mixed</option>
        </select>
      </div>
      <div className="form-actions">
        <button className="btn btn-secondary" onClick={prevStep}>
          Back
        </button>
        <button className="btn btn-primary" onClick={nextStep}>
          Next
        </button>
      </div>
    </>
  )
}
