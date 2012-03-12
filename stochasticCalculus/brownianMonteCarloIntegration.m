function res = brownianMonteCarloIntegration(f, T, tolerance, maxIter)
%   Use Monte Carlo integration to check the formulas from the
%   "Stochastic Calculus and Financial Applications" book
%   from Michael Steele.
%
%   f(time, Bt) = value    
%       A function of the time and "current price" Bt given by the
%       various paths through which we are going. Assumes that f is
%       vectorized with respect to both arguments. You can always wrapped a
%       non-vectorizable function into a fake vectorization wrapper.
%
%   T = 1
%       We integrate over the domain [0,T].
%
%   tolerance = 0.01
%       A constant that determines the number of Monte Carlo estimates that
%       we want to average to get the result. It represents the acceptable
%       variance to the estimate that we are willing to tolerance. Not quite
%       the same thing as the precision of a calculation, though.
%
%   maxIter = 1000
%       The maximal number of paths that we'll use if we can't get the
%       tolerance right.
%
%   There are some constraints here due to the fact that our domain starts
%   at 0 and that all the brownian chains start with value 0, but both
%   these constraints can be avoided if we pick a delayed function f that,
%   for example, really starts at t=10 and is identically 0 before that
%   time. This will produce an integral over paths that are essentially "10
%   time units old". The complexity for this should be found OUTSIDE of
%   this integration function here.

    if nargin < 2
        T = 1;
    end
    if nargin < 3
        tolerance = 0.01;
    end
    if nargin < 4
        maxIter = 5;
    end

    nPaths = 10;
    nDomainPartitions = 200;
    done = false;
    
    % This is a basic FSM with variables for states
    %    (estimate_nPaths, estimate_domain, done).
    % (1,0,0) -> (0,1,0) -> (0,0,1).
    estimate_nPaths = true;
    estimate_domain = false;
    
    iter = 1;
    while ~done
        domain = linspace(0, T, nDomainPartitions);
    
        Bt = sampleBrownianMotion_byIncrements(domain, nPaths);
    
        %size(Bt)
        %size(domain)
        %nPaths
        %pause
        functionEvaluationsOnPaths = f(repmat(domain, [nPaths,1]), Bt);
    
        dBt = Bt(:, 2:end) - Bt(:, 1:end-1);
        
        % Could have been functionEvaluationsOnPaths(:, 1:end-1) but it
        % doesn't matter if f is the least bit continuous.
        % This gets the integration estimates over the paths.
        E0 = functionEvaluationsOnPaths(:, 2:end) .* dBt;
        E = sum(E0,2);
        
        if estimate_nPaths
            var(E)/sqrt(nPaths)
            if var(E)/sqrt(nPaths) < tolerance
                estimate_nPaths = false;
                estimate_domain = true;
            else
                nPaths = 2*nPaths;
                fprintf('Increased number of paths to %d\n.', nPaths);
            end
        end
        
        if estimate_domain
            mean(var(E0,1,2))/sqrt(nDomainPartitions)
            if mean(var(E0,1,2))/sqrt(nDomainPartitions) < tolerance
                estimate_domain = false;
                done = true;
            else
                nDomainPartitions = 2*nDomainPartitions;
                fprintf('Increased number of partitions to %d\n.', nDomainPartitions);
            end
        end
        
        % the safety valve
        iter = iter + 1;
        if iter > maxIter
            done = true;
        end
    end
    

    
    res = mean(E);
end






