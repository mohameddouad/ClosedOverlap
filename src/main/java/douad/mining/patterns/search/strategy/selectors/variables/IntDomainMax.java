package douad.mining.patterns.search.strategy.selectors.variables;

import org.chocosolver.solver.search.strategy.selectors.values.IntValueSelector;
import org.chocosolver.solver.variables.IntVar;

/**
 * Selects the variable upper bound
 * <br/>
 *
 * @author Douad Mohamed El Amine
 * @since mars. 2023
 */

public final class IntDomainMax implements IntValueSelector {

    @Override
    public int selectValue(IntVar var) {
        return var.getUB();
    }

}