% =============================================================================
% PROVENANCE  asi_octave/run_asi.m  (driver; OURS.  It contains no sampler code)
% -----------------------------------------------------------------------------
% Purpose: call the authors' ORIGINAL, UNMODIFIED ASI_sampler.m (Griffin,
%   Latuszynski & Steel 2021, Biometrika 108(1):53-69, DOI 10.1093/biomet/
%   asaa055; code "Version3.0", sha256 of ASI_sampler.m
%   4705c79523f4d772625764bcb880ed04852d83d121ea94fe46ef224d3b10dddb) under GNU
%   Octave, for ../fit_asi.R.  fit_asi.R checks the sha256 before every run.
% What this file does, and nothing else:
%   1. reads the work directory from the environment variable ASI_OCTAVE_WORKDIR;
%   2. reads params.txt ("name value" lines), sampler_dir.txt, X.bin, y.bin
%      (raw doubles, column-major), all written by fit_asi.R;
%   3. puts the sampler's directory on the path (shims, if any, would go on the
%      path here too; none is needed, see ../README.md);
%   4. seeds Octave's generators: rand("state", seed) and randn("state", seed).
%      "state" selects the Mersenne Twister and initialises it from the scalar
%      seed (Octave manual, rand).  ASI_sampler.m draws with rand only (randn
%      is reached only when updateg == 1, which is not used);
%   5. calls ASI_sampler with its 18 arguments, in the order of line 1 of
%      ASI_sampler.m.  data_fixed is an n x 0 matrix (no forced covariates);
%   6. writes the fields of the returned struct, unchanged, as raw doubles, and
%      the sampler's wall time (tic/toc around the call).
%   0. before anything else, turns off Octave's workspace dump on a signal
%      (crash_dumps_octave_core, sigterm_dumps_octave_core,
%      sighup_dumps_octave_core).  Without this a killed run writes the file
%      "octave-workspace" (X, y and all sampler state) into the directory the
%      harness was started from.  It changes nothing in a run that completes.
% No value is set here: every argument comes from params.txt, i.e. from
% fit_asi.R, whose PROVENANCE block gives the source of each.
% =============================================================================
crash_dumps_octave_core(false);
sigterm_dumps_octave_core(false);
sighup_dumps_octave_core(false);
workdir = getenv("ASI_OCTAVE_WORKDIR");
if isempty(workdir) || ~exist(workdir, "dir")
  error("run_asi: ASI_OCTAVE_WORKDIR is not set or is not a directory");
end

% ---- parameters -------------------------------------------------------------
P = struct();
fid = fopen(fullfile(workdir, "params.txt"), "r");
if fid < 0, error("run_asi: cannot open params.txt"); end
while true
  ln = fgetl(fid);
  if ~ischar(ln), break; end
  tok = strsplit(strtrim(ln), " ");
  if numel(tok) == 2
    P.(tok{1}) = str2double(tok{2});
  end
end
fclose(fid);
need = {"n", "p", "seed", "g", "gprior", "mode", "RB_adap", "RB", "hparam", "tau", "nu", ...
        "burnin", "numbofits", "thin", "numbofreps", "heat", "adap_type", "updateg"};
for i = 1:numel(need)
  if ~isfield(P, need{i}) || isnan(P.(need{i}))
    error(["run_asi: parameter missing or not a number: " need{i}]);
  end
end
fid = fopen(fullfile(workdir, "sampler_dir.txt"), "r");
sampler_dir = strtrim(fgetl(fid));
fclose(fid);

% ---- data -------------------------------------------------------------------
fid = fopen(fullfile(workdir, "X.bin"), "r");
[data, cnt] = fread(fid, [P.n, P.p], "double");
fclose(fid);
if cnt ~= P.n * P.p, error("run_asi: X.bin has the wrong length"); end
fid = fopen(fullfile(workdir, "y.bin"), "r");
[target, cnt] = fread(fid, [P.n, 1], "double");
fclose(fid);
if cnt ~= P.n, error("run_asi: y.bin has the wrong length"); end
data_fixed = zeros(P.n, 0);

% ---- the authors' sampler ---------------------------------------------------
addpath(sampler_dir);
w = which("ASI_sampler");
fid = fopen(fullfile(workdir, "which_sampler.txt"), "w"); fprintf(fid, "%s\n", w); fclose(fid);
rand("state", P.seed);
randn("state", P.seed);
t0 = tic;
output = ASI_sampler(data_fixed, data, target, P.g, P.gprior, P.mode, P.RB_adap, P.RB, P.hparam, ...
                     P.tau, P.nu, P.burnin, P.numbofits, P.thin, P.numbofreps, P.heat, P.adap_type, P.updateg);
sampler_sec = toc(t0);

% ---- results, as returned ---------------------------------------------------
function wr(workdir, name, v)
  fid = fopen(fullfile(workdir, [name ".bin"]), "w");
  fwrite(fid, double(v(:)), "double");
  fclose(fid);
end
wr(workdir, "prob_inclusion", output.prob_inclusion);
wr(workdir, "prob_inclusion2", output.prob_inclusion2);
wr(workdir, "logpost", output.logpost);
wr(workdir, "modelsize", output.modelsize);
wr(workdir, "accept", output.accept);
wr(workdir, "zeta", output.zeta);
wr(workdir, "zetaAS", output.zetaAS);
wr(workdir, "zetaDS", output.zetaDS);
wr(workdir, "g_out", output.g);
fid = fopen(fullfile(workdir, "done.txt"), "w");
fprintf(fid, "octave_version %s\n", OCTAVE_VERSION());
fprintf(fid, "sampler_sec %.6f\n", sampler_sec);
fprintf(fid, "blas %s\n", version("-blas"));
fclose(fid);
