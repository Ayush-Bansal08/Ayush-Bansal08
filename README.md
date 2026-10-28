<p align="center">
  <img src="https://raw.githubusercontent.com/Ayush-Bansal08/Ayush-Bansal08/main/assets/banner.svg" alt="Ayush Bansal — Software Engineer. Backend systems, cloud platforms, applied AI. Build. Verify. Ship." width="100%" />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/ayush-bansal-21b12a311/">LinkedIn</a> &nbsp;·&nbsp;
  <a href="mailto:ab262133@gmail.com">Email</a> &nbsp;·&nbsp;
  <a href="https://github.com/Ayush-Bansal08?tab=repositories">All repositories</a>
</p>

## Hi, I'm Ayush

I build backend services, Kubernetes platforms, and AI tools with an emphasis on **verification, failure handling, and clear operational trade-offs**.

Previously a **Software Engineering Intern at Finn (Airforge Tech)** and an **AI/ML Research Intern at UNSW Sydney**. Studying Electronics & Communication Engineering at **LNMIIT Jaipur, Class of 2028**.

**Open to software engineering internships and opportunities in backend, cloud, platform, and AI engineering.**

## Three projects to start with

### 01 / [Helios — Kubernetes Developer Platform](https://github.com/Ayush-Bansal08/k8s-project)

**Go · Kubernetes · ArgoCD · Argo Rollouts · Prometheus · Azure**

A platform for deploying containerized workloads through GitOps, evaluating canary releases against Prometheus metrics, and provisioning preview environments with a custom Go operator.

- **The implementation:** a `PreviewEnvironment` custom resource creates a namespace, Deployment, Service, and Ingress; deletion triggers finalizer-based namespace cleanup.
- **The delivery path:** declarative ArgoCD applications, staged canary rollouts, and a Prometheus success-rate analysis template.
- **The scope:** a portfolio platform using Online Boutique and Podinfo as existing workloads.

[Go controller](https://github.com/Ayush-Bansal08/k8s-project/blob/main/operator/internal/controller/previewenvironment_controller.go) · [Canary analysis](https://github.com/Ayush-Bansal08/k8s-project/blob/main/apps/podinfo-canary/analysistemplate.yaml) · [Architecture](https://github.com/Ayush-Bansal08/k8s-project#-architecture) · [Video walkthrough](https://drive.google.com/file/d/14-x45ra9iRBMOevZ0CqfLridM_HQqiSa/view?usp=sharing)

### 02 / [DockHealer — Dockerfile Generation with Verification](https://github.com/Ayush-Bansal08/Dockhealer)

**Python · Docker · Ollama · Terraform · pytest**

A local-LLM CLI that generates Dockerfiles and checks them through **deterministic validation → Docker build → container smoke test**, with a bounded repair loop.

- **The implementation:** failure classification, retry budgets, repeated-failure detection, and a human-required stop for project-level dependency faults.
- **The verification:** 186 documented automated tests using injected fakes; real Docker/Ollama evaluation is a separate, reproducible workflow.
- **The boundary:** hardened smoke containers and redaction reduce risk; Docker builds still execute code and require trusted input.

[Source](https://github.com/Ayush-Bansal08/Dockhealer/tree/main/src/dockhealer) · [Tests](https://github.com/Ayush-Bansal08/Dockhealer/tree/main/tests) · [Evaluation protocol](https://github.com/Ayush-Bansal08/Dockhealer/blob/main/docs/EVAL_PROTOCOL.md) · [Security model](https://github.com/Ayush-Bansal08/Dockhealer#security-model)

### 03 / [PollForge — Event-Driven Voting on Azure](https://github.com/Ayush-Bansal08/PollForge)

**Python · C# / .NET · Node.js · Redis · PostgreSQL · AKS**

A five-service voting stack: Flask queues votes in Redis, a .NET worker persists them in PostgreSQL, and Node.js broadcasts live results over Socket.IO.

- **The infrastructure:** Kubernetes workloads, StatefulSet-backed PostgreSQL storage, TLS configuration, and Prometheus monitoring.
- **The delivery path:** GitHub Actions builds SHA-tagged images for ACR and deploys to AKS using Azure OIDC.
- **The trade-off:** asynchronous processing gives eventual consistency; the README documents the current queue-loss window and production hardening work.

[Architecture](https://github.com/Ayush-Bansal08/PollForge#architecture) · [Deployment workflow](https://github.com/Ayush-Bansal08/PollForge/blob/main/.github/workflows/deploy.yaml) · [Kubernetes manifests](https://github.com/Ayush-Bansal08/PollForge/tree/main/k8s-specifications) · [Video walkthrough](https://drive.google.com/file/d/1pVh277Bao5hEftS_H58uTEaM6GU1tDl0/view?usp=sharing)

<sub>Cloud demo environments may be stopped when idle. Source, architecture, and configuration remain available for review.</sub>

## Experience

| Role | Work |
| --- | --- |
| **Software Engineering Intern · Finn / Airforge Tech**<br>May–July 2026 · Bengaluru | 25+ merged PRs across 5+ production services: AI voice agents, backend APIs, authentication, WhatsApp automation, and dashboards. Built LLM workflows and worked on staging and production delivery with Docker, Kubernetes, Nginx, and CI/CD. |
| **AI/ML Research Intern · UNSW Sydney**<br>May–August 2026 · Remote | Worked with Dr. Rohitash Chandra on hyperspectral mineral exploration using SOMs and autoencoders. Corrected a training defect that improved reported mineral recall from 0% to 76.6%; audited eight pipeline bugs and developed evaluation with sweeps, significance tests, stability analysis, and ablations. |

## Engineering toolkit

| Focus | Tools I use |
| --- | --- |
| **Backend & data** | Python, TypeScript / JavaScript, Node.js, Express, Flask, PostgreSQL, Redis, MongoDB, REST APIs, WebSockets |
| **Cloud & platforms** | Go / Kubebuilder, Docker, Kubernetes, Azure, AKS, ACR, Terraform, Helm, Linux |
| **Delivery & operations** | GitHub Actions, ArgoCD, Argo Rollouts, OIDC, Nginx, Prometheus, Grafana, Trivy, Kyverno |
| **AI & evaluation** | Ollama, LangChain, Hugging Face, scikit-learn, NumPy, Pandas, pytest |

## Recognition

**LNMHacks 8.0 · Partner Prize Winner · January 2026**  
Won the Viral Consumer Apps track — **$600 prize**, among **500+ participants**.

---

Interested in **backend systems, developer infrastructure, and reliable AI tooling**?  
[Let's connect on LinkedIn](https://www.linkedin.com/in/ayush-bansal-21b12a311/) or [email me](mailto:ab262133@gmail.com).
