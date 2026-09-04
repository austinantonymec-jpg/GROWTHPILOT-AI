import random
def simulate(sessions=100, seed=None):
    rng=random.Random(seed); baseline_orders=[]; agent_orders=[]; accepted=0
    for _ in range(sessions):
        base=rng.randint(700,2800); converts=rng.random()<.31
        if converts: baseline_orders.append(base)
        accepted_offer=converts and rng.random()<.46
        if accepted_offer: accepted+=1; agent_orders.append(int(base*(1+rng.uniform(.16,.36))))
        elif converts or rng.random()<.035: agent_orders.append(base)
    base_rev=sum(baseline_orders); agent_rev=sum(agent_orders); discount_cost=round(agent_rev*.018)
    return {"sessions":sessions,"assumptions":{"baseline_conversion":"31%","agent_conversion_lift":"3.5pp eligible sessions; accepted bundles add 16–36% AOV","discount_cap":"10% (simulation average 1.8% revenue cost)"},"baseline":{"orders":len(baseline_orders),"conversion_rate":round(len(baseline_orders)/sessions*100,1),"revenue":base_rev,"average_order_value":round(base_rev/max(1,len(baseline_orders)))},"agent":{"orders":len(agent_orders),"conversion_rate":round(len(agent_orders)/sessions*100,1),"revenue":agent_rev,"average_order_value":round(agent_rev/max(1,len(agent_orders))),"recommendations_accepted":accepted},"recommendation_acceptance_rate":round(accepted/max(1,len(agent_orders))*100,1),"discount_cost":discount_cost,"net_revenue_impact":agent_rev-discount_cost-base_rev,"revenue_uplift_percent":round((agent_rev/base_rev-1)*100,1) if base_rev else 0}
if __name__ == "__main__": print(simulate())
