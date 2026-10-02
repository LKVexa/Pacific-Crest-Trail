/* User-authored physical records and labelled fiction remain separate service-owned domains. */
'use strict';
(() => {
  const get=id=>document.getElementById(id);
  const api=window.dossierApi;
  const actions=['assignment','workout','preparation','decision','journal'];
  const state={context:null,data:null,loading:false,saving:false,pending:null,pendingConfirmed:false,loadSequence:0,drafts:new Map(),loadedPendingCampaign:null};
  const forms=Object.fromEntries(actions.map(action=>[action,get(`${action}-form`)]));
  const number=value=>Number(value).toLocaleString('en-US',{maximumFractionDigits:2});
  const known=value=>typeof value==='number'&&Number.isFinite(value);
  const nullable=value=>value===''?null:Number(value);
  const storageKey=campaign=>`trail.experience.pending.${location.host}.${campaign}`;

  function announce(message,type='') {
    get('experience-status').textContent=message;
    get('experience-status').className=`experience-status ${type}`.trim();
  }

  function emitEligibility() {
    const data=state.data;
    const matched=Boolean(data&&state.context&&data.day_id===state.context.stage.id);
    const blocked=state.loading||state.saving||Boolean(state.pending)||!matched;
    const reasons=blocked?[state.pending?'A training or story save is awaiting confirmation.':state.saving?'Saving the day record…':state.loading?'Loading the saved day requirements…':'Reconnect to load the saved day requirements.']:(data?.eligibility?.missing || data?.eligibility?.reasons || []);
    window.dispatchEvent(new CustomEvent('trail:eligibility',{detail:{day_id:state.context?.stage.id,eligible:!blocked&&data?.eligibility?.eligible===true,reasons,experience_revision:data?.experience_revision}}));
  }

  function writable() {
    return Boolean(state.context?.nonce&&state.context.trail?.current_day_id===state.context.stage.id&&state.data?.eligibility?.current_day===true&&!state.loading&&!state.saving&&!state.pending);
  }

  function updateAvailability() {
    const enabled=writable();
    Object.values(forms).forEach(form=>form.querySelector('fieldset').disabled=!enabled);
    if(state.data?.preparation)forms.preparation.querySelector('fieldset').disabled=true;
    if(state.data?.decision)forms.decision.querySelector('fieldset').disabled=true;
    const walking=get('assignment-category').value==='walking';
    get('assignment-targets').hidden=!walking;
    get('assignment-duration').disabled=!walking;
    get('assignment-distance').disabled=!walking;
    get('assignment-unit').disabled=!walking;
    get('journal-empty').disabled=Boolean(get('journal-text').value.trim());
    if(get('journal-text').value.trim())get('journal-empty').checked=false;
    get('experience-pending').hidden=!state.pending;
    get('experience-retry').disabled=state.saving;
    if(state.pending)get('experience-pending-copy').textContent=`The ${state.pending.action} save for Day ${Number(state.pending.body.day_id.slice(4))} is ${state.pendingConfirmed?'committed, but its current records still need refreshing':'awaiting confirmation'}. Check this same save before starting another.`;
    emitEligibility();
  }

  function retainDrafts() {
    if(!state.context)return;
    const draft={};
    for(const action of actions) {
      draft[action]={};
      forms[action].querySelectorAll('input,select,textarea').forEach(field=>{
        if(field.id && field.type!=='radio')draft[action][field.id]=field.type==='checkbox'?field.checked:field.value;
      });
    }
    const selected=forms.decision.querySelector('input[name="story-option"]:checked');
    draft.selectedOption=selected?.value || '';
    state.drafts.set(state.context.stage.id,draft);
  }

  function restoreDraft(action) {
    const draft=state.drafts.get(state.context.stage.id)?.[action];
    if(!draft)return false;
    Object.entries(draft).forEach(([id,value])=>{const field=get(id);if(field){if(field.type==='checkbox')field.checked=Boolean(value);else field.value=value;}});
    return true;
  }

  function clearDraft(action,dayId) {
    const draft=state.drafts.get(dayId);if(draft)delete draft[action];
  }

  function assignmentSummary(assignment) {
    if(!assignment)return 'No accepted assignment. You can choose your own plan or review the dossier as preparation.';
    const parts=[assignment.title || 'Your assignment',assignment.activity_category];
    if(known(assignment.duration_minutes))parts.push(`${number(assignment.duration_minutes)} min target`);
    if(known(assignment.distance))parts.push(`${number(assignment.distance)} ${assignment.distance_unit} target`);
    return `Saved: ${parts.join(' · ')}`;
  }

  function renderAssignment() {
    const assignment=state.data?.assignment;
    get('saved-assignment').textContent=assignmentSummary(assignment);
    if(!restoreDraft('assignment')) {
      get('assignment-category').value=assignment?.activity_category || 'walking';
      get('assignment-title').value=assignment?.title || '';
      get('assignment-duration').value=assignment?.duration_minutes ?? '';
      get('assignment-distance').value=assignment?.distance ?? '';
      get('assignment-unit').value=assignment?.distance_unit || 'mi';
      get('assignment-notes').value=assignment?.notes || '';
    }
    forms.assignment.querySelector('button[type="submit"]').textContent=assignment?'Accept my revised assignment':'Accept my assignment';
  }

  function renderActivity() {
    const totals=state.data?.actual_totals;
    get('actual-totals').replaceChildren();
    for(const [label,value] of [['Known distance subtotal',known(totals?.distance_meters)?`${number(totals.distance_meters/1609.344)} mi`:'Unknown'],['Known duration subtotal',known(totals?.duration_minutes)?`${number(totals.duration_minutes)} min`:'Unknown']]) {
      const card=document.createElement('div');const name=document.createElement('span');name.textContent=label;const amount=document.createElement('strong');amount.textContent=value;card.append(name,amount);get('actual-totals').append(card);
    }
    if((totals?.distance_unknown_count || 0)>0||(totals?.duration_unknown_count || 0)>0) {
      const note=document.createElement('p');note.className='subtotal-note';
      note.textContent=`Unknown distance in ${totals.distance_unknown_count || 0} entr${totals.distance_unknown_count===1?'y':'ies'}; unknown duration in ${totals.duration_unknown_count || 0} entr${totals.duration_unknown_count===1?'y':'ies'}. Subtotals include known measurements only.`;
      get('actual-totals').append(note);
    }
    restoreDraft('workout');
    const records=Array.isArray(state.data?.workouts)?state.data.workouts:[];
    const history=[];
    for(const workout of records) {
      const p=document.createElement('p');
      const values=[workout.purpose?.replaceAll('_',' ') || 'Manual activity'];
      if(known(workout.distance))values.push(`${number(workout.distance)} ${workout.distance_unit}`);
      if(known(workout.duration_minutes))values.push(`${number(workout.duration_minutes)} min`);
      if(!known(workout.distance)&&!known(workout.duration_minutes))values.push('quantities unknown');
      if(workout.activity_date)values.push(workout.activity_date);
      p.textContent=values.join(' · ');
      if(workout.notes){const notes=document.createElement('span');notes.textContent=workout.notes;p.append(notes);}
      history.push(p);
    }
    if(!history.length){const p=document.createElement('p');p.textContent='No actual activity has been saved for this day.';history.push(p);}
    if(state.data?.more_workouts){const p=document.createElement('p');p.textContent='Showing the latest saved activity records; totals include the whole day.';history.push(p);}
    get('workout-history').replaceChildren(...history);
  }

  function renderStory() {
    const scenario=state.data?.scenario;
    get('story-heading').textContent=scenario?.title || 'The daily fictional scene';
    get('story-assumptions').textContent=scenario?.assumptions || '';
    get('story-lesson').textContent=scenario?.lesson_prompt || '';
    get('story-training-reference').textContent=scenario?.training_reference || 'Story choices never change real training targets.';
    const resources=state.data?.resources;
    get('story-resources').textContent=resources?`Fictional planning tokens: ${number(resources.planning_tokens)} · Insight stamps: ${number(resources.insight_stamps)}`:'Fictional counters are unavailable.';
    const options=[];
    const selected=state.drafts.get(state.context.stage.id)?.selectedOption;
    for(const option of Array.isArray(scenario?.options)?scenario.options:[]) {
      const label=document.createElement('label');label.className='story-option';
      const radio=document.createElement('input');radio.type='radio';radio.name='story-option';radio.value=option.id;radio.required=true;
      const affordable=known(resources?.planning_tokens)&&known(option.cost_planning_tokens)&&resources.planning_tokens>=option.cost_planning_tokens;
      radio.disabled=!affordable;radio.checked=selected===option.id;
      const copy=document.createElement('span');const title=document.createElement('strong');title.textContent=option.label;
      const cost=document.createElement('small');cost.textContent=`${number(option.cost_planning_tokens)} fictional token${option.cost_planning_tokens===1?'':'s'} · ${number(option.insight_stamps)} insight stamp${option.insight_stamps===1?'':'s'}${affordable?'':' · Not enough fictional tokens'}`;
      const outcome=document.createElement('small');outcome.textContent=`Story outcome: ${option.outcome}`;
      copy.append(title,cost,outcome);label.append(radio,copy);options.push(label);
    }
    if(scenario?.defer_allowed) {
      const label=document.createElement('label');label.className='story-option defer-option';
      const radio=document.createElement('input');radio.type='radio';radio.name='story-option';radio.value='__defer';radio.required=true;radio.checked=selected==='__defer';
      const span=document.createElement('span');const title=document.createElement('strong');title.textContent='Deliberately defer this optional fictional scene';
      const note=document.createElement('small');note.textContent='No token cost and no physical target changes.';span.append(title,note);label.append(radio,span);options.push(label);
    }
    get('story-options').replaceChildren(...options);
    restoreDraft('decision');
    const decision=state.data?.decision;
    get('saved-decision').hidden=!decision;
    get('saved-decision').textContent=decision?`Saved fictional ${decision.deferred?'deferral':'choice'}: ${decision.outcome?.text || ''}`:'';
    if(decision) {
      const selectedRadio=forms.decision.querySelector(`input[value="${decision.deferred?'__defer':CSS.escape(decision.option_id || '')}"]`);
      if(selectedRadio)selectedRadio.checked=true;
      get('decision-ack').checked=true;
    }
  }

  function renderJournal() {
    const journal=state.data?.journal;
    get('reflection-prompt').textContent=state.data?.scenario?.reflection_prompt || 'What did you notice or learn? A deliberate empty reflection is allowed.';
    get('saved-reflection-panel').hidden=!journal;
    get('saved-reflection').textContent=journal?(journal.text?.trim()?journal.text:'Empty reflection deliberately acknowledged.'):'';
    if(!restoreDraft('journal')){get('journal-text').value=journal?.text || '';get('journal-empty').checked=Boolean(journal?.acknowledge_empty&&!journal?.text?.trim());}
  }

  function renderData() {
    const data=state.data;
    get('experience-mode').textContent=data?.eligibility?.current_day?'CURRENT DAY · EDITABLE':'READ ONLY · DOSSIER REVIEW';
    renderAssignment();renderActivity();renderStory();renderJournal();restoreDraft('preparation');
    get('saved-preparation').textContent=data?.preparation?'Preparation review is saved. This record adds no physical distance.':'';
    if(data?.preparation)get('preparation-ack').checked=true;
    const criteria=[['Participation: preparation review or eligible walking activity',data?.eligibility?.participation_met],['Fictional choice or acknowledged deferral',data?.eligibility?.decision_met],['Saved reflection or deliberate empty reflection',data?.eligibility?.journal_met]];
    get('experience-criteria').replaceChildren(...criteria.map(([label,met])=>{const li=document.createElement('li');li.className=met?'criterion-met':'criterion-unmet';li.textContent=`${met?'Saved':'Required'} — ${label}`;return li;}));
    updateAvailability();
  }

  async function loadDay({announceLoaded=true}={}) {
    if(!state.context?.trail){state.data=null;state.loading=false;announce('Connect to the local service to read or save this day’s records.','error');updateAvailability();return;}
    const day=state.context.stage.id,sequence=++state.loadSequence;
    state.loading=true;updateAvailability();
    try {
      const data=await api.request(`/api/experience?day=${encodeURIComponent(day)}`);
      if(sequence!==state.loadSequence||day!==state.context?.stage.id)return;
      if(data.day_id!==day||data.campaign_id!==state.context.trail.campaign_id||!Number.isInteger(data.experience_revision))throw new Error('The saved experience did not match this day and campaign.');
      state.data=data;
      if(announceLoaded&&!state.pending)announce(data.eligibility?.current_day?'Your saved day records are ready. Each save below is deliberate; nothing advances the day automatically.':'This section is read only. Return to your current day to record activity or make a story choice.');
    }catch(error){if(sequence===state.loadSequence){state.data=null;announce(`${error.message} Your unsent inputs have been preserved in this browser. Reconnect before saving.`,'error');}}
    finally{if(sequence===state.loadSequence){state.loading=false;renderData();}}
  }

  function persistPending(pending) {
    state.pending=pending;
    try {const key=storageKey(state.context.trail.campaign_id);if(pending)localStorage.setItem(key,JSON.stringify(pending));else localStorage.removeItem(key);}catch{if(pending)announce('Browser draft storage is unavailable. Keep this page open to reconcile the pending save; the repository remains authoritative.','error');}
  }

  function restorePending(campaign) {
    if(state.loadedPendingCampaign===campaign)return;
    state.loadedPendingCampaign=campaign;
    try {
      const item=JSON.parse(localStorage.getItem(storageKey(campaign)) || 'null');
      if(item&&item.campaign_id===campaign&&actions.includes(item.action)&&/^day-\d{3,}$/.test(item.body?.day_id)&&/^[A-Za-z0-9_-]{12,128}$/.test(item.body?.operation_id)&&Number.isInteger(item.body.expected_experience_revision)&&Number.isInteger(item.body.expected_campaign_revision))state.pending=item;
    }catch{/* Optional browser draft storage cannot define repository state. */}
  }

  function payload(action) {
    if(action==='assignment') {
      const category=get('assignment-category').value;
      return {activity_category:category,title:get('assignment-title').value || 'My accepted assignment',notes:get('assignment-notes').value,
        distance:category==='walking'?nullable(get('assignment-distance').value):null,distance_unit:category==='walking'&&get('assignment-distance').value!==''?get('assignment-unit').value:null,
        duration_minutes:category==='walking'?nullable(get('assignment-duration').value):null};
    }
    if(action==='workout') {
      const value={purpose:get('workout-purpose').value,notes:get('workout-notes').value,distance:nullable(get('workout-distance').value),
        distance_unit:get('workout-distance').value!==''?get('workout-unit').value:null,duration_minutes:nullable(get('workout-duration').value)};
      if(get('workout-date').value)value.activity_date=get('workout-date').value;
      if(get('workout-timezone').value.trim())value.timezone=get('workout-timezone').value.trim();
      return value;
    }
    if(action==='preparation')return {reviewed_dossier:true};
    if(action==='decision') {
      const option=forms.decision.querySelector('input[name="story-option"]:checked')?.value;
      if(!option)throw new Error('Choose a fictional option or deliberate deferral first.');
      return option==='__defer'?{deferred:true,acknowledged:true}:{option_id:option,acknowledged:true};
    }
    const text=get('journal-text').value;
    if(!text.trim()&&!get('journal-empty').checked)throw new Error('Write a reflection or deliberately acknowledge an empty one.');
    return {text,expected_journal_revision:state.data.journal?.revision || 0,acknowledge_empty:!text.trim()&&get('journal-empty').checked};
  }

  async function acceptReceipt(result) {
    const pending=state.pending;
    if(!result?.ok||result.operation_id!==pending?.body.operation_id||result.receipt?.operation_id!==pending.body.operation_id||result.receipt?.day_id!==pending.body.day_id||result.receipt?.action!==pending.action)throw new Error('The response did not confirm this exact day record.');
    state.pendingConfirmed=true;
    const data=result.experience || await api.request(`/api/experience?day=${encodeURIComponent(pending.body.day_id)}`);
    if(data.day_id!==pending.body.day_id||data.campaign_id!==pending.campaign_id||!Number.isInteger(data.experience_revision))throw new Error('The saved receipt is confirmed, but its refreshed records did not match.');
    persistPending(null);state.pendingConfirmed=false;
    clearDraft(pending.action,pending.body.day_id);
    if(state.context.stage.id===pending.body.day_id) {
      state.data=data;
      if(pending.action==='workout'){forms.workout.reset();}
      if(pending.action==='decision'){const draft=state.drafts.get(pending.body.day_id);if(draft)delete draft.selectedOption;}
      renderData();
    }
    announce(`Saved ${pending.action==='workout'?'actual activity':pending.action==='decision'?'fictional choice or deferral':pending.action==='journal'?'camp reflection':pending.action==='preparation'?'preparation review':'your assignment'} for Day ${Number(pending.body.day_id.slice(4))}. The virtual day has not been completed.`,'success');
  }

  async function submitPending({lookupFirst=false}={}) {
    if(!state.pending||state.saving)return;
    state.saving=true;updateAvailability();announce('Checking the authoritative save…');
    try {
      if(lookupFirst) {
        try {const result=await api.request(`/api/operations/${encodeURIComponent(state.pending.body.operation_id)}`);await acceptReceipt(result);return;}
        catch(error){if(error.status!==404)throw error;}
      }
      if(!state.context.nonce) {
        const bootstrap=await api.request('/api/bootstrap');
        if(bootstrap.campaign_id!==state.pending.campaign_id)throw new Error('The campaign changed. Reload and review the saved trail before retrying.');
        state.context.nonce=bootstrap.nonce;state.context.trail=bootstrap;
      }
      const pending=state.pending;
      const result=await api.request(`/api/${pending.action}`,{method:'POST',headers:{'Content-Type':'application/json','X-PCT-Nonce':state.context.nonce},body:JSON.stringify(pending.body)});
      await acceptReceipt(result);
    }catch(error) {
      if(state.pendingConfirmed) {
        announce('The save is committed, but current records could not be refreshed. Check the same save after reconnecting.','error');
      }else if(error.status===409) {
        persistPending(null);state.pendingConfirmed=false;
        await api.refreshState({silent:true});
        await loadDay({announceLoaded:false});
        get('saved-reflection-panel').open=true;
        announce(`${error.message} Your proposed inputs are preserved. Compare the refreshed saved records, then deliberately save again if appropriate.`,'error');
      }else if(error.status>=400&&error.status<500&&![401,403,408,429].includes(error.status)) {
        persistPending(null);state.pendingConfirmed=false;
        announce(`${error.message} The record was rejected. Your proposed inputs remain available to correct.`,'error');
      }else {
        if([401,403].includes(error.status))state.context.nonce=null;
        announce(state.pendingConfirmed?'The save is committed, but current records could not be refreshed. Check the same save after reconnecting.':`${error.message} This save is awaiting confirmation. Check and retry the same operation; do not submit a replacement.`,'error');
      }
    }finally {state.saving=false;updateAvailability();}
  }

  async function saveAction(action,event) {
    event.preventDefault();
    if(!writable()||!forms[action].reportValidity())return;
    try {
      retainDrafts();
      const operation=crypto.randomUUID?crypto.randomUUID():Array.from(crypto.getRandomValues(new Uint8Array(16)),byte=>byte.toString(16).padStart(2,'0')).join('');
      const body={day_id:state.context.stage.id,operation_id:operation,expected_experience_revision:state.data.experience_revision,
        expected_campaign_revision:state.context.trail.revision,...payload(action)};
      persistPending({campaign_id:state.context.trail.campaign_id,action,body});
      await submitPending();
    }catch(error){announce(error.message,'error');updateAvailability();}
  }

  for(const action of actions) {
    forms[action].addEventListener('submit',event=>saveAction(action,event));
    forms[action].addEventListener('input',()=>{retainDrafts();updateAvailability();});
    forms[action].addEventListener('change',()=>{retainDrafts();updateAvailability();});
  }
  get('experience-retry').addEventListener('click',()=>submitPending({lookupFirst:true}));
  get('reflection-revert').addEventListener('click',()=>{clearDraft('journal',state.context.stage.id);get('journal-text').value=state.data?.journal?.text || '';get('journal-empty').checked=Boolean(state.data?.journal?.acknowledge_empty&&!state.data?.journal?.text?.trim());retainDrafts();updateAvailability();announce('The reflection editor now shows the saved text.');});
  async function handleDay(event) {
    const next=event.detail;
    if(!next?.stage)return;
    const same=state.context?.stage.id===next.stage.id&&state.context?.trail?.campaign_id===next.trail?.campaign_id;
    const unchanged=same&&state.context?.trail?.revision===next.trail?.revision&&state.context?.nonce===next.nonce;
    if(state.context)retainDrafts();
    state.context=next;
    if(next.trail)restorePending(next.trail.campaign_id);
    if(!same) {
      state.data=null;
      Object.values(forms).forEach(form=>form.reset());
      get('story-options').replaceChildren();get('saved-decision').hidden=true;get('saved-reflection-panel').hidden=true;
      announce('Loading this day’s saved records…');
    }
    if(unchanged&&state.data){updateAvailability();return;}
    await loadDay();
    if(state.pending&&!state.saving)submitPending({lookupFirst:true});
  }
  window.addEventListener('trail:day',handleDay);
  updateAvailability();
  if(window.dossierCurrentContext)handleDay({detail:window.dossierCurrentContext});
})();
