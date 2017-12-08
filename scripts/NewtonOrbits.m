its = size(Positions, 1);
points = size(Positions, 2);

for i=1:(its)
    subplot(1, 2, 1)
    scatter3(log(Positions(i, :)), (i-1)*ones(1, points), Positions(1, :), 30, Positions(1, :));
    xlabel('LogPosition'); ylabel('Iteration'); zlabel('Color');
    xlim([min(min(log(Positions))), max(max(log(Positions)))]); ylim([0, its]);
    hold on
    subplot(1, 2, 2)
    scatter3(Positions(1, :), (i-1)*ones(1, points), log(Density(i, :) + 1));
    xlabel('Position'); ylabel('Iteration'); zlabel('Log(Density + 1)');
    ylim([0, its]);
    hold on
end
hold off