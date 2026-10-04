import React, { useEffect, useState } from "react";
import { api } from "./api";
import {
  LayoutDashboard, Factory, FileCheck2, GitBranch, Clock3,
  Gift, RefreshCcw, ShieldCheck, ArrowRight, CheckCircle2,
  AlertTriangle, UploadCloud
} from "lucide-react";

const menu = [
  ["dashboard", "Dashboard", LayoutDashboard],
  ["mapper", "Approval Mapper", Factory],
  ["documents", "Document Validator", FileCheck2],
  ["applications", "Applications", GitBranch],
  ["sla", "SLA Monitor", Clock3],
  ["renewals", "Renewals & Incentives", Gift],
];

function App() {
  const [page, setPage] = useState("dashboard");
  const [summary, setSummary] = useState(null);
  const [apps, setApps] = useState([]);
  const [profile, setProfile] = useState(null);
  const [approvals, setApprovals] = useState([]);
  const [selectedApproval, setSelectedApproval] = useState(null);
  const [docs, setDocs] = useState([]);
  const [message, setMessage] = useState("");

  const load = async () => {
    try {
      const [s, a, p] = await Promise.all([
        api.dashboard(), api.applications(), api.profiles(1)
      ]);
      setSummary(s); setApps(a); setProfile(p);
    } catch (e) { setMessage("Start the backend/database first. " + e.message); }
  };

  useEffect(() => { load(); }, []);

  const generateMap = async () => {
    try {
      const data = await api.approvalMap(profile.id);
      setApprovals(data);
      setMessage(`${data.length} applicable approvals identified.`);
    } catch (e) { setMessage(e.message); }
  };

  const createApplication = async (approvalId) => {
    try {
      await api.createApplication({ profile_id: profile.id, approval_id: approvalId });
      await load();
      setMessage("Application submitted and workflow created.");
    } catch (e) { setMessage(e.message); }
  };

  const showDocs = async (approvalId) => {
    setSelectedApproval(approvalId);
    setDocs(await api.approvalDocs(approvalId));
    setPage("documents");
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brandMark">C</div>
          <div><b>CIVIC@ME</b><span>Smart industrial approvals</span></div>
        </div>
        <nav>
          {menu.map(([id, label, Icon]) => (
            <button className={page === id ? "nav active" : "nav"} onClick={() => setPage(id)} key={id}>
              <Icon size={18}/>{label}
            </button>
          ))}
        </nav>
        <div className="sideCard">
          <ShieldCheck size={18}/>
          <b>SIH26130</b>
          <span>Government of Maharashtra</span>
        </div>
      </aside>

      <main>
        <header>
          <div>
            <p className="eyebrow">INTELLIGENT APPROVALS</p>
            <h1>{menu.find(x => x[0] === page)?.[1] || "Dashboard"}</h1>
          </div>
          <div className="profilePill"><span className="dot"/> Demo Applicant</div>
        </header>

        {message && <div className="notice">{message}</div>}

        {page === "dashboard" && <Dashboard summary={summary} apps={apps} setPage={setPage}/>}
        {page === "mapper" && <Mapper profile={profile} approvals={approvals} generateMap={generateMap} createApplication={createApplication} showDocs={showDocs}/>}
        {page === "documents" && <Documents docs={docs} selectedApproval={selectedApproval}/>}
        {page === "applications" && <Applications apps={apps}/>}
        {page === "sla" && <SLA/>}
        {page === "renewals" && <Renewals/>}
      </main>
    </div>
  );
}

function Dashboard({summary, apps, setPage}) {
  if (!summary) return <Empty text="Loading dashboard…"/>;
  return <>
    <section className="hero">
      <div><span className="badge">MVP • Smart Automation</span><h2>One guided journey for every industrial approval.</h2>
      <p>Discover approvals, validate documents, route workflows and track statutory timelines from one place.</p></div>
      <button className="primary" onClick={() => setPage("mapper")}>Start approval mapping <ArrowRight size={17}/></button>
    </section>
    <div className="cards">
      <Metric label="Applications" value={summary.total_applications} icon={GitBranch}/>
      <Metric label="Pending" value={summary.pending} icon={Clock3}/>
      <Metric label="Approved" value={summary.approved} icon={CheckCircle2}/>
      <Metric label="Overdue" value={summary.overdue} icon={AlertTriangle}/>
    </div>
    <section className="grid2">
      <div className="panel"><h3>Current applications</h3>{apps.map(a => <ApplicationRow key={a.id} a={a}/>)}</div>
      <div className="panel"><h3>Platform workflow</h3>
        {["Business profile","Approval discovery","Document validation","Parallel processing","Inspection","SLA tracking","Renewal + incentives"].map((x,i)=>
          <div className="flow" key={x}><span>{String(i+1).padStart(2,"0")}</span><b>{x}</b>{i<6 && <ArrowRight size={15}/>}</div>)}
      </div>
    </section>
  </>;
}

function Mapper({profile, approvals, generateMap, createApplication, showDocs}) {
  return <section>
    <div className="panel">
      <div className="sectionHead"><div><h2>Smart Approval Mapper</h2><p>Rules use sector, location, project size and operating stage.</p></div>
      <button className="primary" onClick={generateMap}>Generate checklist</button></div>
      {profile && <div className="profileGrid">
        <div><small>Business</small><b>{profile.name}</b></div>
        <div><small>Sector</small><b>{profile.sector}</b></div>
        <div><small>Location</small><b>{profile.location}</b></div>
        <div><small>Size</small><b>{profile.project_size}</b></div>
        <div><small>Stage</small><b>{profile.operating_stage}</b></div>
      </div>}
    </div>
    <div className="panel"><h3>Applicable approvals</h3>
      {approvals.length === 0 ? <Empty text="Click “Generate checklist” to run the approval rules."/> :
      approvals.map(a => <div className="approval" key={a.id}>
        <div className="seq">{a.sequence}</div><div className="grow"><b>{a.name}</b><span>{a.department} • SLA {a.sla_days} days</span><p>{a.description}</p></div>
        <button className="secondary" onClick={() => showDocs(a.id)}>Documents</button>
        <button className="primary small" onClick={() => createApplication(a.id)}>Apply</button>
      </div>)}
    </div>
  </section>;
}

function Documents({docs, selectedApproval}) {
  const [filename, setFilename] = useState("project-report.pdf");
  const [result, setResult] = useState(null);
  const validate = async (id) => {
    try { setResult(await api.validateDocument({requirement_id:id, filename})); }
    catch(e) { setResult({status:"rejected", validation_message:e.message}); }
  };
  return <section className="panel"><h2>Document & Application Validator</h2>
    <p>Prototype pre-check: required document + file type/filename validation. OCR/content checks can be plugged into this endpoint later.</p>
    {docs.length === 0 ? <Empty text="Choose “Documents” from an approval in the mapper."/> :
    docs.map(d => <div className="doc" key={d.id}><FileCheck2 size={19}/><div className="grow"><b>{d.name}</b><span>Required: {d.required ? "Yes" : "No"}</span></div>
      <input value={filename} onChange={e=>setFilename(e.target.value)} /><button className="secondary" onClick={()=>validate(d.id)}><UploadCloud size={15}/> Validate</button></div>)}
    {result && <div className={result.status === "validated" ? "successBox" : "errorBox"}><b>{result.status}</b><span>{result.validation_message}</span></div>}
  </section>;
}

function Applications({apps}) {
  return <section className="panel"><h2>Application Workflow</h2>{apps.map(a => <ApplicationRow key={a.id} a={a} detailed/>)}</section>;
}

function ApplicationRow({a, detailed}) {
  return <div className="appRow"><div className="statusIcon">{a.sla_state==="overdue" ? <AlertTriangle/> : <CheckCircle2/>}</div>
    <div className="grow"><b>{a.reference_no}</b><span>{a.approval_name} • {a.department}</span>{detailed && <div className="bar"><i style={{width:a.status==="approved"?"100%":"55%"}}/></div>}</div>
    <span className={"status "+a.sla_state}>{a.status.replace("_"," ")}</span><span className="due">{a.due_date}</span></div>
}

function SLA() {
  const [rows,setRows]=useState([]);
  useEffect(()=>{api.sla().then(setRows).catch(()=>{});},[]);
  return <section className="panel"><div className="sectionHead"><div><h2>SLA Intelligence</h2><p>Track statutory/service timelines and surface bottlenecks.</p></div></div>
    {rows.map(r=><div className="slaRow" key={r.reference_no}><b>{r.reference_no}</b><span>{r.status}</span><span>{r.due_date}</span><strong className={r.days_remaining<0?"red":""}>{r.days_remaining<0?`${Math.abs(r.days_remaining)} days overdue`:`${r.days_remaining} days left`}</strong></div>)}
  </section>;
}

function Renewals() {
  const [renewals,setRenewals]=useState([]); const [incentives,setIncentives]=useState([]);
  useEffect(()=>{api.renewals().then(setRenewals); api.incentives().then(setIncentives);},[]);
  return <section className="grid2"><div className="panel"><h2>Renewals</h2>{renewals.map(r=><div className="listItem" key={r.id}><RefreshCcw size={18}/><div><b>{r.approval_name}</b><span>Renewal: {r.renewal_date}</span></div></div>)}</div>
    <div className="panel"><h2>Incentives & support</h2>{incentives.map(i=><div className="listItem" key={i.id}><Gift size={18}/><div><b>{i.name}</b><span>{i.description}</span></div></div>)}</div></section>;
}

function Metric({label,value,icon:Icon}) { return <div className="metric"><Icon/><small>{label}</small><strong>{value}</strong></div> }
function Empty({text}) { return <div className="empty">{text}</div> }

export default App;
