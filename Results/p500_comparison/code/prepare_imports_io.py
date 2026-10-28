"""Local artifact copying/hash verification only; no numerical aggregation."""
import pathlib,hashlib,json,shutil,ast
base=pathlib.Path(__file__).resolve().parents[2];root=pathlib.Path(__file__).resolve().parent
mix=base/'Experiment/Experiments_October_14_Mixture';bench=base/'Experiment/Experiments_October_14_Benchmarks'
final=mix/'metadata/audit_snapshots/final_2208411/summary'
archives=pathlib.Path('C:/Users/felip/Documents/NOTS_Archives/2026-10-14')
bm=archives/'Experiments_October_14_Benchmarks/final20261015T0140ZportableV3'
mm=archives/'Experiments_October_14_Mixture/mixture20261015T1830Zv1'
files={'benchmark':bench/'summary/validated_rows.csv','benchmark_scenario':bench/'summary/scenario_summary.csv',
 'original':mix/'reference/original_bb_verified.csv','pairing':mix/'reference/benchmark_pairing_verified.csv',
 'original_provenance':mix/'reference/original_comparison_provenance.json',
 'mixture':final/'completed_rows_latest.csv','mixture_inventory':final/'inventory_latest.csv',
 'final_bb_scenario':final/'comparison_errors.csv','final_provenance':final/'comparison_provenance.json',
 'final_snapshot_manifest':mix/'metadata/audit_snapshots/final_2208411/snapshot_manifest.json',
 'final_receipt':mix/'metadata/final_completion_receipt.json',
 'benchmark_archive_receipt':bm.with_suffix('.verified.json'),'mixture_archive_receipt':mm.with_suffix('.verified.json'),
 'benchmark_archive_manifest':bm.with_suffix('.manifest.json'),'mixture_archive_manifest':mm.with_suffix('.manifest.json'),
 'baseline_gate':base/'Experiment/Experiments_October_14/metadata/VALIDATION_PASSED.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
dest=root/'inputs';dest.mkdir(exist_ok=True);inputs={}
for role,path in files.items():
 target=dest/(role+path.suffix);assert path.is_file(),path
 if target.exists():assert sha(target)==sha(path)
 else:shutil.copy2(path,target)
 inputs[role]=dict(file=target.relative_to(root).as_posix(),sha256=sha(target),original_local_path=str(path))
assert inputs['benchmark']['sha256']=='bc0845f15bc1b9f818f9220e81f726a786f344c41c54035d40d2367e9ab75b43'
assert inputs['mixture']['sha256']=='76e54a2b6a950d4ee426422b3bdfb7cdbc011b60f083f37cbce3b710caad184b'
bindings={}
for role,manifest_role in [('benchmark','benchmark_archive_manifest'),('benchmark_scenario','benchmark_archive_manifest'),
 ('original','mixture_archive_manifest'),('pairing','mixture_archive_manifest'),('mixture','mixture_archive_manifest'),
 ('mixture_inventory','mixture_archive_manifest'),('final_bb_scenario','mixture_archive_manifest'),('final_provenance','mixture_archive_manifest'),('final_receipt','mixture_archive_manifest')]:
 entries=json.loads((root/inputs[manifest_role]['file']).read_text(encoding='utf-8-sig'))['entries']
 matches=[e for e in entries if e.get('sha256')==inputs[role]['sha256'] and e['type']=='file']
 assert matches,(role,'not bound to archive')
 preferred=next((e for e in matches if '/home/summary/' in e['path']),matches[0])
 bindings[role]=dict(manifest_role=manifest_role,member=preferred['path'])
config=dict(inputs=inputs,json_roles=[r for r in inputs if files[r].suffix=='.json'],archive_bindings=bindings,
 source_seals=dict(benchmark='31af767aa5ae7c52c2455dbe3034968582e39888570f39f02194845953108fde',mixture='ebff4ae31aba4fe7675186df9f0ab1d30d3a68a77c52bec31e680c89fb4e5aea',
 original={k:('b30205ae4f6cda6538870c2af3b65d64d5045119b147ab3d8014546decc58d44' if k=='c100' else 'e0e2332dc79239443a6a3a43a094828ff78d6e12ede53fff2e015a400082af32') for k in ['c100','c075','c050','c035','c025']}),
 authoritative_mixture='final_2208411 current completed rows and inventory; historical paired_subset files excluded',strict_jobs=['2204382','2204775','2204776','2204782','2208411'])
(root/'imports.json').write_text(json.dumps(config,indent=2)+'\n')
ast.parse((root/'compare_all.py').read_text());print('Static syntax and artifact/hash imports verified; no numerical aggregation executed.')
