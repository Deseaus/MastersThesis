--# -path=.:alltenses:../chunk:../style:../translator
concrete WikiHint of Wiki = WikiMaster - [RuleChunk, HintChunk, LookupChunk] ** {

lin RuleChunk r = r.hint ;
lin HintChunk h = h.hint ;
lin LookupChunk l = l.hint ;
}
