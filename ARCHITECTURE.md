ai-evaluation/
├── src/                        # Core execution & tools
│   ├── agent_interface.py      
│   ├── sample_agent.py         
│   ├── attacks.py              
│   ├── logger.py               
│   └── test_runner.py          # Orchestrates the run
│
├── data/                       # Test cases
│   └── test_cases.json         
│
├── evaluation/                 # The Grading & Scoring Engine
│   ├── rule_checks.py          # Keyword filters
│   ├── llm_judge.py            # Fine-tuned model
│   └── metrics_engine.py       # final scores and timings
│
├── fine_tuning/                # Training Pipeline
│   ├── generate_dataset.py     
│   ├── training_dataset.csv    
│   └── Train_Prometheus.ipynb  
│
├── outputs/           
│   ├── final_report.md         
│   └── evaluation.log          
│
├── .env                        
├── .gitignore                  
├── requirements.txt            
├── ARCHITECTURE.md             
└── README.md