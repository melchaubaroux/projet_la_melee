import jiwer

from ressource_wer import excepted_result,whisper_result

def calcul_wer (reference_text,whisper_output):

    # Appliquez les transformations aux deux textes
    transform = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveEmptyStrings(),
        jiwer.RemoveMultipleSpaces()
    ])

    # mise en forme des données 
    reference_words = transform(reference_text.split())
    output_words = transform(whisper_output.split())

    # calcul des longeurs et comparaison 

    reference_text_len=len(reference_words)
    whisper_output_len=len(output_words)

    print(" taille du texte de reference="+str(reference_text_len))
    print(" taille du texte de whisper ="+str(whisper_output_len))

    length_comparaison= whisper_output_len-reference_text_len


    # équilibrage des tailles 
    if reference_text_len < whisper_output_len : 
        reference_words+=[ "remplissage" for x in range(length_comparaison)]

    if reference_text_len > whisper_output_len : 
        output_words+=[ "remplissage" for x in range(-length_comparaison)]


    # Calculez le WER
    wer = jiwer.wer(reference_words, output_words)

    # annonce du resultat 
    result=f"Word Error Rate (WER) : {wer*100.0:.4f}%"

    
    return result

    # Interprétation du résultat :
    # - Un WER proche de 0 indique une excellente précision
    # - Un WER inférieur à 10% est généralement considéré comme bon
    # - Un WER supérieur à 20% peut nécessiter des améliorations


if __name__=="__main__": 

    # test du calcul WER
    reference_text = excepted_result  #"Votre texte de référence ici"
    whisper_output = whisper_result #"Le texte transcrit par Whisper ici"
    test_result= calcul_wer(reference_text,whisper_output)
    print(test_result)
    test_result= calcul_wer(whisper_output,reference_text)
    print(test_result)


