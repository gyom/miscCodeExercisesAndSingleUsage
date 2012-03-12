   nPaths = 10;
   X = sampleBrownianMotion_byIncrements(linspace(0,1, 200), nPaths);
   
   colormap = lines;
   figure, hold on;
   for p=1:nPaths
       plot(X(p,:), 'Color', colormap(rem(p, size(colormap,1)),:), 'LineWidth', 1)
   end
   
   
   
   f = @(t,Bt) (Bt);
   T = 1;
   tolerance = 0.01;
   maxIter = 1000;
   
   res = brownianMonteCarloIntegration(f, T, tolerance, maxIter);
   
   A = 10; B = 5;
   T = 1;
   maxIter = 10;
   tolerance = 0.01;
   res = brownianMonteCarloIntegration(makeStoppingTimeIndicator(-B,A), T, tolerance, maxIter);
   
   
   
   res = brownianMonteCarloIntegration(makeStoppingTimeIndicator(-1,2), T, tolerance, maxIter);
   
   res = brownianMonteCarloIntegration(@(t,Bt) (t < 0.5), T, tolerance, maxIter);
   