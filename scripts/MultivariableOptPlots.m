v = VideoWriter('Multivariable Nesterov (Rosenbrock)', 'Motion JPEG AVI');
v.FrameRate = 12;
v.Quality = 100;
open(v);
timesteps = size(Times, 2);
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
figure();
for i=1:timesteps
    scatter(Positions(:, 1, i), Positions(:, 2, i), 30, linspace(0, 1, size(Positions, 1)))
    xlim([-2, 2]); ylim([-2, 2.1647]);
%     hold on
    xlabel('X Positions'); ylabel('Y Positions'); title(['Time = ' num2str(Times(1, i))]);
    frame = getframe(gcf);
    writeVideo(v, frame);
end
% hold off
close(v);

v = VideoWriter('Multivariable Nesterov Density(Rosenbrock)', 'Motion JPEG AVI');
v.FrameRate = 12;
v.Quality = 100;
open(v);
timesteps = size(Times, 2);
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
figure();
tri = delaunay(DensitySamps(:, 1), DensitySamps(:, 2));
for i=1:timesteps
    trisurf(tri, DensitySamps(:, 1), DensitySamps(:, 2), log(Density(:, i)+1))
    shading interp
    xlim([-2, 2]); ylim([-2, 2.1647]); zlim([0, 4.25]);
    xlabel('X Positions'); ylabel('Y Positions'); zlabel('log(Density + 1)'); title(['Time = ' num2str(Times(1, i))]);
    frame = getframe(gcf);
    writeVideo(v, frame);
end
close(v);
