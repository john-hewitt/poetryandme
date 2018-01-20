# poetryandme
Interactive poetry generation

## Data locations

 - Raw sonnets at `data/sonnets.raw`.
 - Sonnets where each quatrain is on one line and each sonnet is demarked by a blank line at `data/sonnets.qtr`.

## Training the model

        python backend/nn.py data/training_data.json vocabs.json

###Prediction toy pipeline

        python backend/predictor.py model.pt vocabs.json 
        
