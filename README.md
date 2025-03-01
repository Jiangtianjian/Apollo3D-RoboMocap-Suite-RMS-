# Apollo3D RoboMocap Suite (RMS)
# Robot Motion Capture Suite
* Only Use for single agent
* Synchronous Mode is needed

Author: Kuihan Chen[Team Apollo3D].
> Use Method：
>
> Default:
>
> ```python3 proxy.py```
>
> Custom Port:
>
> ```python3 proxy.py -s [toServerPort] -a [toAgentPort]```
    

* Further Development Upon Apollo3D RMS
```python
        # Get Status
        acc = world.worldModel_dict('ACC')
        j_head1 = world.perceptor_dict('hj1')
        e_head1 = world.effector_dict('he1')

        # Deal with List
        def deal_serverList(serverList):
            pass
        
        def deal_agentList(agentList):
            pass
        
```
