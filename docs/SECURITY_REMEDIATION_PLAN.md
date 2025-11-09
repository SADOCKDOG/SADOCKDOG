# Security Remediation Plan (Backend Container)

> Status: Draft – prepared ahead of gated vulnerability run.
> Scope: Backend runtime image (after hardening: Node binary only, no npm/npx nor global node_modules).

## 1. Summary
The container security workflow now fails (`exit-code: 1`) if CRITICAL or HIGH vulnerabilities remain. This plan provides a prioritized path to remediate findings while preserving build stability.

## 2. Assumed Current Findings (Placeholder until next run)
| Package            | Severity  | CVE              | Runtime Impact | Present After Hardening? | Notes |
|--------------------|-----------|------------------|----------------|--------------------------|-------|
| cross-spawn        | HIGH      | CVE-2024-21538   | Build-time only (removed from final) | TBD | Verify absence in new SBOM |
| starlette          | MEDIUM/HIGH? | CVE-2025-62727 | FastAPI dependency | Likely | May need FastAPI bump |
| h2 (http/2 lib)    | MEDIUM    | CVE-2025-57804   | Potential indirect (check SBOM) | TBD | Confirm actual inclusion |
| brace-expansion    | LOW       | CVE-2025-5889    | Build-time only (removed) | TBD | Should disappear |

## 3. Decision Matrix
| Action | Criteria | Tool/Step | Success Metric |
|--------|----------|----------|----------------|
| FastAPI/Starlette patch | Starlette CVE confirmed & fixed upstream | `poetry update fastapi starlette` | SBOM shows patched versions, no HIGH for starlette |
| Remove transitive JS vulns | Node libs only needed during build | Already removed from final stage | SBOM: no cross-spawn, brace-expansion |
| Validate Prisma node requirement | If node binary later shown vulnerable | Consider moving Prisma generation to multi-stage leaving engine only | SBOM: no extraneous Node packages |
| Monitor new CVEs daily | Scheduled run at 03:00 UTC | Actions schedule | Alerts triaged <24h |

## 4. Remediation Steps
### 4.1 Verify Removal of Build-Time JS Libraries
1. Run latest container workflow (manual or wait for schedule).
2. Download `sbom-backend.json`.
3. Use script:
   ```powershell
   pwsh ./scripts/compare_security_artifacts.ps1 -OldSbom .\container-scan-backend\sbom-backend-prev.json -NewSbom .\container-scan-backend\sbom-backend.json
   ```
4. Confirm absence of `cross-spawn`, `brace-expansion`.

### 4.2 Patch Python Dependencies
1. Inspect SARIF for `starlette` or `fastapi` vulnerable versions.
2. Edit `autogpt_platform/backend/pyproject.toml` if needed (bump within compatible range).
3. Run:
   ```powershell
   cd autogpt_platform/backend
   poetry lock --no-update   # sanity if only version spec changed
   poetry update fastapi starlette
   poetry run test -x
   ```
4. Re-run container workflow. Gate should pass if no remaining HIGH.

### 4.3 Optional: Further Slimming
If CVE targets Node binary itself:
- Consider copying only Prisma generated artifacts (`.prisma` + engine) and removing Node entirely from final stage.
- Validate migrations run in dedicated builder/migrate stage.

### 4.4 Documentation Update
After remediation:
- Append results to `docs/SECURITY_SCANNING.md` under a new section `Remediation History`:
  ```
  YYYY-MM-DD: Removed build-time vulnerable JS libs from runtime; patched Starlette (CVE-2025-62727).
  ```

## 5. Verification Checklist
| Check | Method | Expected |
|-------|--------|----------|
| Gate passes | GitHub Actions result | ✔ SUCCESS |
| No HIGH/CRITICAL in SARIF | Open SARIF alerts | None listed |
| SBOM diff removal | compare script | cross-spawn, brace-expansion absent |
| FastAPI/Starlette updated | `poetry show fastapi starlette` | Versions >= patched release |

## 6. Rollback Strategy
If an upgrade breaks runtime:
1. Revert dependency bumps (`git revert <commit>`).
2. Pin last known safe versions explicitly.
3. Create issue for deeper refactor or isolation of vulnerable component.

## 7. Next Opportunities
- Integrate `pip-audit` into workflow (Python package CVE scan).
- Add `osv-scanner` for frontend lockfile once frontend scan reinstated.
- Publish SBOM to GHCR alongside image digest (provenance chain).

## 8. PR Instructions
1. Branch: `ci/gitleaks-setup` (already contains this file).
2. Open PR to `dev` with title:
   `ci(platform): add backend security remediation plan`
3. Include checklist: initial findings, steps executed, outcome of next gated run.

## 9. Pending Data
Replace placeholder severities and presence flags after next run:
- Update table in section 2.
- Commit changes referencing run ID.

---
**Maintainer Note:** Do not mark this plan complete until the first gated run passes without intervention.
