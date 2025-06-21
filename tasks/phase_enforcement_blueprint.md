## 🔐 HIMKS Phase Enforcement Blueprint v1

### 🎯 Goal
Ensure that all phase transitions, session prescriptions, and override pathways are:
- Guardrail-compliant
- User-state aware
- Consent-sensitive
- Phase-appropriate

---

### 🧱 Logic Sources Reviewed
- `PHASE_MANAGER.txt`
- `SESSION_ENGINE.txt`
- `SAFETY_OVERRIDES.txt`
- `SPECIAL_POPULATIONS.txt`
- `USER_PROFILE.txt`

---

### ✅ Enforcement Requirements Checklist

#### 1. **Phase Entry Conditions**
- [x] All phase start triggers checked for readiness flags
- [ ] Sleep quality < 65% must delay or modify phase start
- [ ] HRV index below threshold must trigger a phase gate

#### 2. **Session Allocation Overrides**
- [x] Session engine respects illness overrides
- [ ] Add fallback session if user is flagged `MENTAL_FATIGUE_HIGH`
- [ ] Re-check session logic against special populations tags

#### 3. **Consent Flags**
- [ ] `SESSION_ENGINE` must query `USER_PROFILE[consent_override]` for high load weeks
- [x] Pain flags cause fallback as expected

#### 4. **Hardcoded Thresholds to Replace**
- [ ] HRV < 52 is hard-coded; should reference dynamic baseline from `USER_PROFILE`
- [ ] Sleep < 5.5h trigger is embedded; abstract to `SAFETY_OVERRIDES.guardrail('sleep')`

---

### 🔧 Upgrade Recommendations

#### A. Extract Guardrail Thresholds
Create a dynamic guardrail registry:
```python
# safety_constants.py
GUARDRAILS = {
  'sleep': lambda profile: profile['sleep_baseline'] * 0.75,
  'hrv': lambda profile: profile['hrv_baseline'] * 0.85
}
```

#### B. Inject Consent Checks in SESSION_ENGINE
Wrap high load session prescriptions with:
```python
if not user['consent_override']:
    fallback_to_lower_load()
```

#### C. Extend SPECIAL_POPULATIONS Tag Map
Ensure it propagates to session filtering logic:
```python
if user['tags'].includes('joint_recovery'):
    filter_sessions(avoid=['plyometric', 'eccentric overload'])
```

---

### 📦 Next Step
- Implement fixes
- Re-run orchestrator
- Validate with fault replay and feedback simulator

> PR this blueprint using `git_upgrade_coordinator.py` under branch: `upgrade/phase_enforcement_v1`
