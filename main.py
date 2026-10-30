import streamlit as st
import streamlit.components.v1 as components
from rag_engine import VectraEngine, OLLAMA_MODEL

st.set_page_config(
    page_title="Vectra | Intelligence Workspace",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700&display=swap');

html {background:#05060D !important;}
body {background:transparent !important;}
#root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
[data-testid="stMain"] {background: transparent !important;}
.stApp {font-family:'Manrope',sans-serif;}
.block-container {max-width:none !important; padding:2.2rem 5vw 3rem !important;}

h1,h2,h3 {font-family:'Instrument Serif',Georgia,serif !important;
          font-weight:400 !important; letter-spacing:-.01em;}
h1 {font-size:3rem !important;}
h2, [data-testid="stHeading"] h2 {font-size:2.1rem !important;}

/* sidebar */
[data-testid="stSidebar"] {background:rgba(10,11,24,.80) !important;
    backdrop-filter:blur(18px); border-right:1px solid rgba(160,150,255,.16);}
.brand {font-family:'Instrument Serif',serif; font-size:2.2rem; line-height:1;}
.subtle {color:#9A9BB8; font-size:.85rem; margin-top:4px;}

/* hero */
.hero {padding:5vh 0 6vh; max-width:none;}
.hero h1 {font-size:clamp(3.4rem,9vw,9rem) !important; line-height:.95;
          margin:0 0 1.2rem; max-width:13ch;}
.hero h1 em {color:#FFB454;}
.hero p {color:#9A9BB8; font-size:1.25rem; max-width:52ch; margin-bottom:1.6rem;}
.legend {display:flex; flex-wrap:wrap; gap:18px; color:#9A9BB8; font-size:.85rem;}
.legend i {display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:7px;}

/* cards */
.card {background:rgba(14,15,30,.72); border:1px solid rgba(160,150,255,.16);
       border-radius:18px; padding:22px; backdrop-filter:blur(14px); height:100%;}
.card h3 {margin:0 0 6px; font-size:1.6rem !important;}
.card p {color:#9A9BB8; margin:0; font-size:.95rem;}

/* metrics */
[data-testid="stMetric"] {background:rgba(14,15,30,.72);
    border:1px solid rgba(160,150,255,.16); border-radius:16px;
    padding:18px 20px; backdrop-filter:blur(14px);}
[data-testid="stMetricValue"] {font-family:'Instrument Serif',serif; font-size:2rem;}
[data-testid="stMetricLabel"] {color:#9A9BB8;}

/* buttons */
[data-testid="stBaseButton-primary"] {background:#FFB454 !important; color:#1a1100 !important;
    border:0 !important; border-radius:99px !important; font-weight:700 !important;
    transition:transform .15s;}
[data-testid="stBaseButton-primary"] p {color:#1a1100 !important; font-weight:700;}
[data-testid="stBaseButton-primary"]:hover {transform:translateY(-2px);}
[data-testid="stBaseButton-primary"]:disabled {opacity:.4;}
[data-testid="stBaseButton-secondary"] {background:rgba(5,6,13,.5) !important;
    border:1px solid rgba(160,150,255,.16) !important; border-radius:99px !important;}
[data-testid="stBaseButton-secondary"]:hover {border-color:#FF7A7A !important; color:#FF7A7A !important;}

/* inputs */
[data-baseweb="textarea"], [data-baseweb="input"], [data-baseweb="select"] > div {
    background:rgba(255,255,255,.04) !important; border-radius:12px !important;
    border-color:rgba(160,150,255,.16) !important;}
[data-baseweb="textarea"]:focus-within, [data-baseweb="input"]:focus-within {
    border-color:#8B7CFF !important;}
[data-testid="stFileUploaderDropzone"] {background:rgba(255,255,255,.03);
    border:1.5px dashed rgba(139,124,255,.45); border-radius:14px;}
[data-testid="stFileUploaderDropzone"]:hover {border-color:#FFB454;
    background:rgba(255,180,84,.06);}

/* expanders, alerts */
[data-testid="stExpander"] {background:rgba(14,15,30,.72);
    border:1px solid rgba(160,150,255,.16) !important; border-radius:14px;
    backdrop-filter:blur(14px);}
[data-testid="stAlert"] {border-radius:14px; backdrop-filter:blur(10px);}
hr {border-color:rgba(160,150,255,.16) !important;}
a {color:#FFB454;}

/* keep the zero-height 3D mount out of the layout */
[data-testid="stElementContainer"]:has(iframe[height="0"]) {
    position:absolute; height:0; margin:0; overflow:hidden;}

/* no sidebar: navigation lives in the top bar */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"], [data-testid="stAppDeployButton"] {display:none !important;}
.card {height:170px; min-height:170px; height:170px; display:flex; flex-direction:column; justify-content:center;}
[data-testid="stMetric"] {min-height:120px;}

/* top navigation as pills */
[data-testid="stRadio"] [role="radiogroup"] {gap:8px; justify-content:flex-end; flex-wrap:wrap;}
[data-testid="stRadio"] label {background:rgba(14,15,30,.72); border:1px solid rgba(160,150,255,.16);
    border-radius:99px; padding:6px 18px; cursor:pointer; backdrop-filter:blur(14px); transition:.15s;}
[data-testid="stRadio"] label > div:first-child {display:none;}
[data-testid="stRadio"] label:hover {border-color:#FFB454;}
[data-testid="stRadio"] label:has(input:checked) {background:#FFB454; border-color:#FFB454;}
[data-testid="stRadio"] label:has(input:checked) p {color:#1a1100 !important; font-weight:700;}

/* Explore cards: the card itself is the navigation button */
.st-key-explore button {height:170px; min-height:170px; width:100%; padding:22px !important;
    border-radius:18px !important; background:rgba(14,15,30,.72) !important;
    border:1px solid rgba(160,150,255,.16) !important; backdrop-filter:blur(14px);
    transition:transform .2s, border-color .2s;}
.st-key-explore button:hover {border-color:#FFB454 !important; transform:translateY(-3px);}
.st-key-explore button > div {justify-content:flex-start; width:100%;}
.st-key-explore button p {text-align:left; color:#9A9BB8; font-size:.98rem; margin:0; line-height:1.5;}
.st-key-explore button p strong {display:block; font-family:'Instrument Serif',Georgia,serif;
    font-weight:400; font-size:1.8rem; color:#ECEBFA; margin-bottom:6px;}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3D vector-space background (mounted into the page behind everything)
# ---------------------------------------------------------------------------
SCENE_JS = r"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function(){
  var P=window.parent, D;
  try{ D=P.document; D.body; }catch(e){ return; }
  if(!window.THREE) return;
  if(P.__vectraStop) P.__vectraStop();
  var old=D.getElementById("vectra-bg"); if(old) old.remove();

  var canvas=D.createElement("canvas"); canvas.id="vectra-bg";
  canvas.style.cssText="position:fixed;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none;opacity:__OPACITY__";
  D.body.prepend(canvas);

  var alive=true;
  var reduce=P.matchMedia("(prefers-reduced-motion:reduce)").matches;
  var R=new THREE.WebGLRenderer({canvas:canvas,antialias:true,alpha:true});
  R.setPixelRatio(Math.min(P.devicePixelRatio||1,2));
  var S=new THREE.Scene(), C=new THREE.PerspectiveCamera(55,1,.1,100);
  C.position.set(0,0,15);
  var G=new THREE.Group(); S.add(G);

  var sp=document.createElement("canvas"); sp.width=sp.height=64;
  var x=sp.getContext("2d"), g=x.createRadialGradient(32,32,0,32,32,32);
  g.addColorStop(0,"rgba(255,255,255,1)"); g.addColorStop(.35,"rgba(255,255,255,.55)"); g.addColorStop(1,"rgba(255,255,255,0)");
  x.fillStyle=g; x.fillRect(0,0,64,64);
  var tex=new THREE.CanvasTexture(sp);

  var seed=7; function rnd(){ seed=(seed*16807)%2147483647; return (seed-1)/2147483646; }
  function gauss(){ return (rnd()+rnd()+rnd()-1.5)*2; }

  // clusters spread across the whole field, plus a uniform scatter so no area is empty
  var centers=[[-16,6,-4],[-7,-6,-6],[2,7,-8],[10,-5,-2],[18,5,-5],[-2,0,-10]].map(function(a){return new THREE.Vector3(a[0],a[1],a[2]);});
  var palette=[new THREE.Color(0x8B7CFF),new THREE.Color(0x4FD1E8)];
  var N=1100, pos=new Float32Array(N*3), col=new Float32Array(N*3), pts=[];
  for(var i=0;i<N;i++){
    var p, k;
    if(i%10<4){
      k=i%2; p=new THREE.Vector3((rnd()-.5)*64,(rnd()-.5)*34,-16+rnd()*20);
    } else {
      var ci=i%centers.length, c=centers[ci]; k=ci%2;
      p=new THREE.Vector3(c.x+gauss()*3.2,c.y+gauss()*2.6,c.z+gauss()*3);
    }
    pts.push(p); pos[i*3]=p.x; pos[i*3+1]=p.y; pos[i*3+2]=p.z;
    var cc=palette[k].clone().multiplyScalar(.55+rnd()*.45);
    col[i*3]=cc.r; col[i*3+1]=cc.g; col[i*3+2]=cc.b;
  }
  var geo=new THREE.BufferGeometry();
  geo.setAttribute("position",new THREE.BufferAttribute(pos,3));
  geo.setAttribute("color",new THREE.BufferAttribute(col,3));
  G.add(new THREE.Points(geo,new THREE.PointsMaterial({size:.32,map:tex,vertexColors:true,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending})));

  var probe=new THREE.Group(); G.add(probe);
  probe.add(new THREE.Mesh(new THREE.IcosahedronGeometry(.55,1),new THREE.MeshBasicMaterial({color:0xFFB454,wireframe:true})));
  probe.add(new THREE.Mesh(new THREE.SphereGeometry(.2,16,16),new THREE.MeshBasicMaterial({color:0xFFE0A8})));
  var halo=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,color:0xFFB454,transparent:true,opacity:.7,blending:THREE.AdditiveBlending,depthWrite:false}));
  halo.scale.set(3.2,3.2,1); probe.add(halo);

  var K=8, lg=new THREE.BufferGeometry();
  lg.setAttribute("position",new THREE.BufferAttribute(new Float32Array(K*6),3));
  G.add(new THREE.LineSegments(lg,new THREE.LineBasicMaterial({color:0xFFB454,transparent:true,opacity:.55,blending:THREE.AdditiveBlending})));
  var hg=new THREE.BufferGeometry();
  hg.setAttribute("position",new THREE.BufferAttribute(new Float32Array(K*3),3));
  G.add(new THREE.Points(hg,new THREE.PointsMaterial({size:.65,map:tex,color:0xffffff,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending})));

  var ring=new THREE.Mesh(new THREE.RingGeometry(.95,1,64),new THREE.MeshBasicMaterial({color:0xFFB454,transparent:true,opacity:0,side:THREE.DoubleSide,depthWrite:false}));
  G.add(ring);
  var pt=0; // pulse on load and on every click

  var target=0, mx=0, my=0, hasMouse=false;
  var ray=new THREE.Vector3(), wp=new THREE.Vector3();
  probe.position.copy(centers[3]);
  var timer=setInterval(function(){ target=(target+1)%centers.length; },5200);
  function onMove(e){ mx=e.clientX/P.innerWidth-.5; my=e.clientY/P.innerHeight-.5; hasMouse=true; }
  function onDown(){ pt=0; }
  function size(){
    R.setSize(P.innerWidth,P.innerHeight,false);
    C.aspect=P.innerWidth/P.innerHeight; C.updateProjectionMatrix(); C.updateMatrixWorld();
  }
  P.addEventListener("pointermove",onMove);
  P.addEventListener("pointerdown",onDown);
  P.addEventListener("resize",size);
  size();

  P.__vectraStop=function(){
    alive=false; clearInterval(timer);
    P.removeEventListener("pointermove",onMove); P.removeEventListener("pointerdown",onDown);
    P.removeEventListener("resize",size);
    try{R.dispose();}catch(e){}
  };

  var f=0, t0=performance.now();
  function frame(){
    if(!alive) return;
    var t=(performance.now()-t0)/1000;
    // gentle sway only, so the field always fills the screen
    G.rotation.y+=((reduce?0:Math.sin(t*.12)*.18)+mx*.12-G.rotation.y)*.04;
    G.rotation.x+=(my*.08-G.rotation.x)*.04;
    G.updateMatrixWorld();
    if(hasMouse){
      // cast the cursor onto the z=0 plane and move the orb there
      ray.set(mx*2,-my*2,.5).unproject(C).sub(C.position).normalize();
      wp.copy(C.position).addScaledVector(ray,(0-C.position.z)/ray.z);
      G.worldToLocal(wp);
      probe.position.lerp(wp,.12);
    } else {
      var dest=centers[target].clone().add(new THREE.Vector3(Math.sin(t)*1.2,Math.cos(t*.8),0));
      probe.position.lerp(dest,.025);
    }
    probe.rotation.y=t*.8; probe.rotation.x=t*.5;
    halo.material.opacity=.55+Math.sin(t*3)*.15;
    if(f++%4===0){
      var d=pts.map(function(p,i){return [p.distanceToSquared(probe.position),i];})
               .sort(function(a,b){return a[0]-b[0];}).slice(0,K);
      var lp=lg.attributes.position.array, hp=hg.attributes.position.array;
      d.forEach(function(e,j){
        var p=pts[e[1]];
        lp.set([probe.position.x,probe.position.y,probe.position.z,p.x,p.y,p.z],j*6);
        hp.set([p.x,p.y,p.z],j*3);
      });
      lg.attributes.position.needsUpdate=true; hg.attributes.position.needsUpdate=true;
    }
    if(pt<1){
      pt+=.016; ring.position.copy(probe.position); ring.quaternion.copy(C.quaternion);
      var sc=1+pt*9; ring.scale.set(sc,sc,sc); ring.material.opacity=(1-pt)*.8;
    } else ring.material.opacity=0;
    R.render(S,C);
    P.requestAnimationFrame(frame);
  }
  frame();
})();
</script>
"""


def mount_scene(focus: bool):
    """Mount the 3D scene behind the app. `focus` = full brightness
    (Overview); otherwise dimmer so working pages stay readable."""
    components.html(
        SCENE_JS.replace("__OPACITY__", "1" if focus else ".5"),
        height=0
    )


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
@st.cache_resource
def get_engine():
    return VectraEngine()


engine = get_engine()


@st.cache_data(ttl=20)
def ollama_status():
    """Cheap health check (no model run), cached for 20 seconds."""
    return engine.ollama_status()


# ---------------------------------------------------------------------------
# Top bar: brand, navigation, Knowledge Hub
# ---------------------------------------------------------------------------
PAGES = ["Overview", "Ask Vectra", "Insight Lab", "Trust & Evaluation"]
st.session_state.setdefault("page", "Overview")


def go(target):
    st.session_state["page"] = target


brand_col, nav_col = st.columns([1, 3])
with brand_col:
    st.markdown(
        '<div class="brand">Vectra</div>'
        '<div class="subtle">Intelligence workspace</div>',
        unsafe_allow_html=True
    )
with nav_col:
    page = st.radio(
        "Workspace", PAGES, key="page",
        horizontal=True, label_visibility="collapsed"
    )

with st.expander(
    "📚 Knowledge Hub: upload and manage documents",
    expanded=(engine.count_chunks() == 0)
):
    hub_a, hub_b = st.columns([2, 1])

    with hub_a:
        uploads = st.file_uploader(
            "Upload your documents",
            type=["pdf", "docx", "txt", "md"],
            accept_multiple_files=True
        )

        if st.button(
            "Index documents",
            type="primary",
            use_container_width=True,
            disabled=not uploads
        ):
            with st.spinner("Extracting text and creating embeddings..."):
                result = engine.ingest(uploads)

            st.success(
                f"Added {result['documents']} documents "
                f"and {result['chunks']} chunks."
            )

            for error in result["errors"]:
                st.warning(error)

    with hub_b:
        st.caption(f"Documents: {engine.count_documents()}")
        st.caption(f"Evidence chunks: {engine.count_chunks()}")

        if engine.count_chunks():
            st.markdown("**Manage index**")
            confirm = st.checkbox("I want to delete all indexed documents")
            if st.button("Clear index", disabled=not confirm):
                engine.clear_index()
                st.session_state.pop("answer", None)
                st.session_state.pop("sources", None)
                st.rerun()

mount_scene(focus=(page == "Overview"))

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------
if page == "Overview":
    st.markdown(
        '<div class="hero">'
        '<h1>Every answer has a <em>source.</em></h1>'
        '<p>Vectra turns your documents into a map of meaning, finds the '
        'passages closest to your question, and answers with citations you '
        'can check.</p>'
        '<div class="legend">'
        '<span><i style="background:#FFB454"></i>Your question</span>'
        '<span><i style="background:#fff"></i>Passages it retrieved</span>'
        '<span><i style="background:#8B7CFF"></i>Passages from your documents</span>'
        '</div></div>',
        unsafe_allow_html=True
    )

    status = ollama_status()
    mode_label = {
        "ready": f"Ollama ready ({OLLAMA_MODEL})",
        "model_missing": "Model not pulled",
        "offline": "Ollama offline"
    }[status]

    c1, c2, c3 = st.columns(3)
    c1.metric("Documents", engine.count_documents())
    c2.metric("Knowledge chunks", engine.count_chunks())
    c3.metric("AI mode", mode_label)

    if status == "offline":
        st.warning(
            "Ollama is not running. Start it with `ollama serve` "
            "(or open the Ollama app). Retrieval still works without it."
        )
    elif status == "model_missing":
        st.warning(f"Run `ollama pull {OLLAMA_MODEL}` to download the model.")

    st.write("")
    st.subheader("Explore Vectra")
    cards = [
        ("🔎 Ask your knowledge",
         "Find answers grounded in your documents.", "Ask Vectra"),
        ("⚖️ Insight Lab",
         "Compare multiple sources and discover differences.", "Insight Lab"),
        ("🛡️ Trust Center",
         "Test retrieval and inspect supporting evidence.",
         "Trust & Evaluation"),
    ]
    with st.container(key="explore"):
        for col, (title, desc, target) in zip(st.columns(3), cards):
            with col:
                st.button(
                    f"**{title}**  \n{desc}", key=f"open_{target}",
                    use_container_width=True, on_click=go, args=(target,)
                )

    st.write("")
    st.info("Open the Knowledge Hub above to add documents and begin.")

# ---------------------------------------------------------------------------
# Ask Vectra
# ---------------------------------------------------------------------------
elif page == "Ask Vectra":
    st.title("Ask Vectra")
    st.caption(
        "Answers use retrieved passages. Verify important claims "
        "against the original documents."
    )

    question = st.text_area(
        "What would you like to investigate?",
        placeholder="Compare the main findings in my research papers...",
        height=100
    )

    top_k = st.slider("Evidence passages", 2, 10, 5)

    if st.button("Find evidence and answer", type="primary"):
        if not question.strip():
            st.warning("Enter a question.")
        elif engine.count_chunks() == 0:
            st.warning("Upload and index a document first.")
        else:
            with st.spinner("Retrieving evidence and generating answer..."):
                answer, sources = engine.answer(question, top_k)

            st.session_state["answer"] = answer
            st.session_state["sources"] = sources

    if st.session_state.get("answer"):
        st.subheader("Answer")
        st.markdown(st.session_state["answer"])

        st.subheader("Supporting evidence")
        for i, source in enumerate(st.session_state.get("sources", []), 1):
            with st.expander(
                f"[{i}] {source['document']} — "
                f"{source['location']} | score {source['score']:.2f}"
            ):
                st.write(source["text"])
                st.caption(
                    "Similarity is a ranking score, not a probability "
                    "that the answer is correct."
                )

# ---------------------------------------------------------------------------
# Insight Lab
# ---------------------------------------------------------------------------
elif page == "Insight Lab":
    st.title("Insight Lab")
    st.write(
        "Compare indexed documents, identify differences, and "
        "generate a research-style report."
    )

    documents = engine.list_documents()

    if len(documents) < 2:
        st.info("Upload at least two documents to compare them.")
    else:
        selected = st.multiselect(
            "Documents to compare",
            documents,
            default=documents[:min(3, len(documents))]
        )

        focus = st.text_input(
            "Comparison focus",
            "Main findings, similarities, differences, and contradictions"
        )

        if st.button("Generate comparison", type="primary"):
            if len(selected) < 2:
                st.warning("Select at least two documents.")
            else:
                with st.spinner("Comparing the selected sources..."):
                    report, evidence = engine.compare(selected, focus)

                st.markdown(report)

                with st.expander("Inspect the evidence used"):
                    for item in evidence:
                        st.markdown(
                            f"**{item['document']} — {item['location']}**"
                        )
                        st.write(item["text"])

# ---------------------------------------------------------------------------
# Trust & Evaluation
# ---------------------------------------------------------------------------
elif page == "Trust & Evaluation":
    st.title("Trust & Evaluation Center")
    st.write(
        "Check whether retrieval returns useful evidence. "
        "This is a manual smoke test, not a complete benchmark."
    )

    c1, c2 = st.columns(2)
    c1.metric("Documents indexed", engine.count_documents())
    c2.metric("Chunks indexed", engine.count_chunks())

    query = st.text_input(
        "Test question",
        placeholder="Enter a question with a known answer..."
    )

    if st.button("Test retrieval"):
        if not query.strip():
            st.warning("Enter a question.")
        elif not engine.count_chunks():
            st.warning("Upload a document first.")
        else:
            results = engine.retrieve(query, top_k=5)

            if results:
                st.success(f"Retrieved {len(results)} passages.")

                for i, item in enumerate(results, 1):
                    st.markdown(
                        f"**{i}. {item['document']} — "
                        f"{item['location']}** "
                        f"(score {item['score']:.3f})"
                    )
                    st.write(item["text"])
            else:
                st.error("No evidence was retrieved.")

    st.subheader("Project evaluation checklist")

    checklist = [
        "Correct answers have supporting source passages",
        "Unsupported questions are handled honestly",
        "Citations point to the correct documents and pages",
        "Different documents can be compared",
        "Scanned PDFs and extraction errors are handled appropriately",
        "Prompt injection in document text is tested",
        "Retrieval accuracy and response time are measured"
    ]

    for item in checklist:
        st.checkbox(item, key=item)


st.divider()
st.caption(
    "VECTRA · Evidence-first AI knowledge workspace · "
    "Always verify important findings against their original sources."
)
