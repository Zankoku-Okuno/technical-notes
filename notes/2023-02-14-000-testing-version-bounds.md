# Testing Version Bounds

tags: versioning

Normally, when solving dependencies you want to prefer the highest: you want to use the most up-to-date code.
However, when _testing_ your versino bounds, you probably want to prefer lowest: does this lower bound actually contain all the functions I'm interested in?

When you do solve for lowest, then any versions that are solved to be _higher_ than your stated bounds should be printed to you as warnings.
