--# -path=.:alltenses:../chunk:../style:../translator

concrete WikiMaster of Wiki =
SymbolSpa [MkSymb, Symb], ChunkSpa, StyleCat
-- For the rules and hints:
, SeasonSpa, ListSpa, PresentReferenceSpa
** open Prelude, ParadigmsSpa, SyntaxSpa, StyleRules
-- For the rules and hints:
, ManualDeEstilo, Typography, EntitiesSpa
in {

-- CHUNKS
lin RuleChunk r = r.options ;
lin HintChunk h = h.options ;
lin LookupChunk l = l.options ;

-- TEXT 1: History of Artificial Intelligence
---- 1.A. Seasons
lin AvoidSeasons_Hint s = mkStyleHint (mkNP s) W_11_Estaciones ;
---- 1.B. Quotes
lin Quote_Rule p = mkStyleRule guillemet_Surround (double_straight_Surround | double_curly_Surround | single_straight_Surround) p W_12_Comillas ;
---- 1.C. Numbers in words or figures (Not rendered in the Style Grammar)
---- 1.D. Capitalise
lin Capitalise_Hint = mkStyleHint (mkN ((optionalInitCap "gobierno") | (optionalInitCap "gobiernos"))) DPD_Mayúsculas_4_28 ;
---- 1.E. Acronyms
lin USA_Rule = mkStyleRule ("EUA" | "EE. UU.") ("EE.UU." | "USA" | "U.S.A.") DPD_EUA ;
---- 1.F. Historic Present (Not rendered in the Style Grammar)

-- TEXT 2: Charlotte Gyllenhammar
---- 2.A. Lists in chronological order
lin Chronological_Lists_Hint l = mkStyleHint l W_23_Chronological_lists ;
---- 2.B. Avoid deictic and anaphoric expressions that refer to the time of writing
lin Present_Reference_Hint r = mkStyleHint r W_17_Deictic_expressions ;
---- 2.C. Slash sign optionality
lin Slash_Optionality_Lookup = mkStyleLookup (mkStyleHint forward_slash_Str DPD_Barra_b) ;

-- TEXT 3: Garfield
---- 3.A. Excessive digressions
lin Digressions_Hint p = mkStyleHint (brackets_Surround | square_brackets_Surround | em_dash_Surround | en_dash_Surround) p W_2_Digressions ;
---- 3.B. Ordinal abbreviation
lin Ordinal_Abbreviation_Rule = mkStyleRule ("7.º" | "séptimo") (spaceOrdered "7" "º" | spaceOrdered "7" "o" | dotOrdered "7" "o") W_Abr_Puntos_Volados ;
---- 3.C. Numbers in words or figures (Not rendered in the Style Grammar)
---- 3.D. Abu Dabi
lin Abu_Dabi_Rule = mkStyleRule (mkN "Abu Dabi") ((mkN "Abu Dahbi") | (mkN "Abu Dhabi")) DPD_Abu_Dabi ;

oper
-- Opers to help in creating various types of alternatives
    -- OneTwo or OneMiddleTwo
    glueOrJoin : Str -> Str -> Str -> Str = \s1,s2,middle -> (s1 + s2 | s1 + middle + s2) ;
    -- OneTwo or One Two
    spaceOrdered : Str -> Str -> Str = \s1,s2 -> glueOrJoin s1 s2 " " ;
    -- OneTwo, One Two, TwoOne or Two One
    spaceUnordered : Str -> Str -> Str = \s1,s2 -> ((spaceOrdered s1 s2) | (spaceOrdered s2 s1)) ;
    -- OneTwo or One.Two
    dotOrdered : Str -> Str -> Str = \s1,s2 -> glueOrJoin s1 s2 "." ;
    -- one or One
    optionalInitCap : Str -> Str = \s -> (s | (toUpperFirst s)) ;
} ;
