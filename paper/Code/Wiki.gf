--# -path=.:alltenses:../chunk:../style:../translator

abstract Wiki = Cat, Chunk, StyleCatAbs 
-- Avoid generating parses for both SymbS and S_Chunk, which complicates the grammar.
, Symbol [Symb, MkSymb]
-- For the rules and hints:
, Season, List, PunctuationAbs, PresentReference
** {

flags startcat = Phr ;

-- CHUNKS
fun RuleChunk : StyleRule -> Chunk ;
fun HintChunk : StyleHint -> Chunk ;
fun LookupChunk : StyleLookup -> Chunk ;

-- TEXT 1: History of Artificial Intelligence
---- 1.A. Seasons
fun AvoidSeasons_Hint : Season -> StyleHint ;
---- 1.B. Quotes
fun Quote_Rule : Phr -> StyleRule ;
---- 1.C. Numbers in words or figures (Not rendered in the Style Grammar)
---- 1.D. Capitalise
fun Capitalise_Hint : StyleHint ;
---- 1.E. Acronyms
fun USA_Rule : StyleRule ;
---- 1.F. Historic Present (Not rendered in the Style Grammar)


-- TEXT 2: Charlotte Gyllenhammar
---- 2.A. Lists in chronological order
fun Chronological_Lists_Hint : PhrList -> StyleHint ;
---- 2.B. Avoid deictic and anaphoric expressions that refer to the time of writing
fun Present_Reference_Hint : PresentRef -> StyleHint ;
---- 2.C. Slash sign optionality
fun Slash_Optionality_Lookup : StyleLookup ;

-- TEXT 3: Garfield
---- 3.A. Excessive digressions
fun Digressions_Hint : Phr -> StyleHint ;
---- 3.B. Ordinal abbreviation
fun Ordinal_Abbreviation_Rule : StyleRule ;
---- 3.C. Numbers in words or figures (Not rendered in the Style Grammar)
---- 3.D. Abu Dabi
fun Abu_Dabi_Rule : StyleRule ;
}
