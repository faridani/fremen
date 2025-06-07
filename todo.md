# TODO 

* Move the core library to a separate repo called FremenCore so users can simply import it
* Replace teh terms 
* Work on better AI integration and planning 
* Integrate with Microsoft OmniParser https://www.microsoft.com/en-us/research/articles/omniparser-v2-turning-any-llm-into-a-computer-use-agent/
* Integrate with UI-TARS, UGround, and AGUVIS
* Browser-use: https://github.com/browser-use/web-ui


More on the libraries mentioned:

Microsoft OmniParser is an open-source screen parsing tool designed to enhance AI agents' ability to interact with graphical user interfaces (GUIs) by converting screenshots into structured, actionable elements. It leverages vision-based models, such as GPT-4V, to identify interactable UI components like icons and buttons, providing precise pixel coordinates and semantic understanding for tasks like clicking or typing. OmniParser supports cross-platform GUI interactions across web, desktop, and mobile environments, making it valuable for automating tasks in diverse applications. Its lightweight, modular design and open-source availability on GitHub make it accessible for developers to integrate into vision-based GUI agents, with performance validated on benchmarks like ScreenSpot-Pro.


*UI-TARS by ByteDance*: This is a native GUI agent model that perceives screenshots and performs human-like interactions, such as keyboard and mouse operations. It integrates perception, reasoning, grounding, and memory into a unified vision-language model, supporting cross-platform use (desktop, mobile, web). You can explore it further at GitHub Repository and Research Paper. 
* https://github.com/bytedance/UI-TARS
* https://arxiv.org/abs/2501.12326


*UGround by OSU NLP Group and Orby AI*: UGround is a universal visual grounding model that locates UI elements by pixel coordinates, trained on large-scale screenshot datasets. It's part of the SeeAct-V framework, enabling purely vision-based GUI agents. Check it out at GitHub Repository and Project Homepage.
https://osu-nlp-group.github.io/UGround/

*AGUVIS by University of Hong Kong and Salesforce Research*: AGUVIS is a unified pure vision-based framework for autonomous GUI agents, operating across web, desktop, and mobile platforms. It uses vision-based observations and includes a large dataset for training, focusing on grounding and reasoning. Learn more at GitHub Repository and Project Page.
